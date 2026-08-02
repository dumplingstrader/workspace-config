# How to Use Graph Engineering to Build a Multi-Factor Alpha Model

**Source:** https://x.com/RohOnChain/status/2080296261576687751
**Author:** Roan (@RohOnChain)
**Published:** Jul 23, 2026
**Note:** This is a promotional/educational article pitching a terminal-based agent orchestration tool called "Slate" (by @wearerandomlabs, randomlabs.ai). Summarized below, not reproduced verbatim.

## Core thesis

Multi-factor investing (the approach used by AQR, Two Sigma, Bridgewater) has historically required a full research team -- factor engineers, statisticians, portfolio construction specialists, risk analysts. The article argues that "graph engineering" (coordinating a set of specialized AI agents via a defined graph of nodes and edges) now lets a solo builder replicate that team.

## The 4-stage progression the article frames everything around

1. **Prompts** -- manual, one-off, nothing persists.
2. **Loops** -- a script wraps a prompt and runs on a schedule; state persists.
3. **Swarms** -- multiple specialized agents run in parallel, coordinated by hand-written glue code.
4. **Graphs** -- the coordination structure itself is described declaratively (nodes = agents, edges = data handoffs); the runtime handles parallelism, waiting, retries, and failure isolation instead of custom glue code.

The author's argument for graphs over hand-rolled swarms: scripts break when one agent must wait on another, when state needs to persist across cycles, or when several loops need to run in parallel on different models. A graph runtime handles all three natively, and a failure is scoped to a single node rather than crashing the whole pipeline.

## The 11-node multi-factor graph architecture

**Factor construction nodes (parallel), one agent per classic academic factor:**
1. Market Beta -- rolling 60-month regression vs. market excess return
2. Size (SMB) -- small-cap vs large-cap spread
3. Value (HML) -- high vs low book-to-market spread
4. Momentum (MOM) -- 12-minus-1-month momentum decile spread
5. Profitability (RMW) -- gross profitability
6. Investment (CMA) -- annual asset growth
7. Low Volatility -- trailing 60-day realized volatility decile spread

**Coordination nodes (sequential), running on a stronger reasoning model:**
8. **Validator** -- Newey-West adjusted t-stats per factor, 10,000-iteration bootstrap, rejects factors with >30% in-sample vs out-of-sample degradation
9. **Regime Auditor** -- segments 20 years of history into 3 regimes via Hidden Markov Model, rejects factors that only work in one regime
10. **Portfolio Constructor** -- combines surviving factors into a long/short portfolio with risk-parity weights, enforcing sector/beta/dollar neutrality
11. **Risk Decomposer** -- regresses the portfolio against the 7 factors plus style/macro factors, reports residual alpha and its t-stat (signal only "counts" if residual alpha t-stat > 2.5)

Design principle emphasized throughout: "the maker never validates the maker's own work" -- factor-construction agents run on a faster/cheaper model (Sonnet), validation/audit/decomposition agents run on a stronger model (Opus).

## Build steps (condensed)

1. Install the tool globally via npm (`@randomlabs/slate`), verify with `--version`.
2. Create a dedicated project directory (state is namespaced per workspace).
3. Launch the tool and connect model providers (`/providers`) -- supports bringing your own subscriptions (e.g. Codex, Copilot).
4. Connect models (`/models`) -- pick a fast tier (Sonnet) for factor agents and a strong-reasoning tier (Opus) for coordination agents.
5. Warm up with two built-in example "Programs" (persistent multi-agent graphs):
   - `/goal` -- runs until a grader model verifies the task is objectively done (maker/checker pattern).
   - `/deepresearch` -- fans a research question out to multiple parallel worker agents that report to a synthesizing orchestrator.
6. Draft the actual multi-factor Program by describing the desired graph in plain English; the tool asks clarifying questions (data source, backtest window, universe, regime classifier) before generating the JavaScript graph definition.
7. Review the rendered graph diagram and interrogate design choices (e.g., why a given node runs on a given model) before running anything.
8. Save and run the Program (`slate run <file>.js`); first run takes 15-25 minutes, later runs are faster since state persists.
9. Set a per-run budget cap (`/budget $30/run`) -- the article notes this cap is advisory/self-reported, not a hard kill switch, since there's no real-time cost metering primitive.
10. Debug by describing failures in plain English rather than reading stack traces; the tool patches the specific failing node (author cites three real breakages: a value agent failing on non-US balance sheets, a momentum agent returning zero signals in certain regimes, and a portfolio constructor violating sector neutrality).

## Runtime behavior once deployed

The Program is configured to fire every 24 hours: the 7 factor agents pull the latest day of data and update their factor series, then the 4 coordination nodes run in sequence. The author notes the validator alone rejects roughly 80% of factors that look promising on a first backtest. A day either produces a tradeable signal (residual alpha t-stat > 2.5) or is logged as "no signal" -- both are treated as useful outcomes, notified via a message (e.g. Slack) each morning.

## Author's closing "Blueprint" (paraphrased)

1. Understand the prompts -> loops -> swarms -> graphs progression.
2. Know the seven factors (market, size, value, momentum, profitability, investment, low-vol).
3. Design the graph as 11 nodes (7 parallel construction + 4 sequential coordination) before writing code.
4. Use different model tiers for construction vs. validation/decomposition.
5. Enforce hard statistical gates (Newey-West t-stat, bootstrap iterations, regime robustness, residual alpha threshold).
6. Build intuition by running the example Programs before drafting a custom one.
7. Expect a multi-month ramp: month 1 is debugging, month 2 is refining factors, month 3+ is where tradeable signals start surviving all 11 nodes.
