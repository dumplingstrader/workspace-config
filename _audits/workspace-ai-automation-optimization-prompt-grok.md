# Workspace AI Automation Optimization Prompt for Grok

```text
Role: You are a pragmatic AI-workflow architect specializing in developer workspaces, agent frameworks, local LLM deployment, macOS/Windows automation, VS Code, and human-in-the-loop safety.

Instructions: Assess my existing three-machine AI development environment and recommend how to automate useful work. Determine whether I should keep OpenClaw, migrate to Hermes Agent, test both, or use neither. Do not optimize for novelty, social-media trends, or maximum agent count. Optimize for completed outcomes, reliability, maintainability, privacy, and sensible use of frontier-model subscriptions.

Think carefully before responding. Use current web research and official primary sources for time-sensitive product claims. Cite direct pages you actually opened. Mark unverified claims as "not verified." Do not treat an agent framework, an LLM, a coding CLI, and an inference server as interchangeable products.

## Context

I have three computers:

- Development Windows workstation: primary VS Code and CLI development machine.
- Gaming Windows workstation: gaming, data collection, and Gods Unchained projects.
- Mac Mini: Apple M4 Pro, 24 GB unified memory, macOS Sequoia 15.7.4. It can remain powered on as an automation worker.

My development workspace is rooted at `E:\_Development`. It is an umbrella workspace containing multiple independent Git repositories, including:

- ControlsBMW: engineering content and social-media system.
- controls-docs: engineering knowledge base.
- Documentation: large work-documentation export and automation projects.
- finances: personal portfolio CLI.
- healthassistant: personal health-tracking application.
- Gaming: several Gods Unchained tools, including analytical and real-asset-related projects.
- openclaw-sandbox: the configuration, skills, memory rules, and operating instructions for an OpenClaw agent on the Mac Mini.
- resource-tools: an indexing and retrieval system for AI skills, prompts, and reference material.

The workspace uses:

- Root and project-specific `CLAUDE.md` and `AGENTS.md` instructions.
- `README.md`, `HANDOFF.md`, and `_TODO.md` as project context files.
- Shared Claude skills and project-specific instructions.
- GitHub for cross-machine synchronization.
- VS Code integrated terminals as the primary interaction surface.

Current development-workstation tools:

- VS Code 1.133.0.
- Claude Code 2.1.238 and its VS Code extension.
- Codex CLI 0.147.0 and OpenAI's VS Code extension.
- Kimi Code CLI 0.29.2.
- Grok CLI is not installed.
- OpenClaw, Ollama, and Hermes are not installed on this Windows workstation.

My normal multi-model workflow is approximately:

1. Give a research or architecture question to one frontier model.
2. Ask another model to independently review the response for factual errors, hallucinated capabilities, and missing constraints.
3. Ask Codex to convert the reviewed result into an implementation plan or execute it.
4. Sometimes ask a vendor-specific model, such as Kimi, to assess compatibility with its own tool.
5. Keep audit documents recording the original prompt, response, independent review, and implementation plan.

This has produced rigorous work, but it can also produce substantial meta-documentation before anything operational is deployed.

## Existing OpenClaw state

OpenClaw was configured as an always-on personal assistant and ControlsBMW persona on the Mac Mini. Its design includes:

- Messaging through Discord and Telegram.
- Heartbeats and cron jobs.
- Persistent memory and daily notes.
- Approximately 58 skills.
- Explicit financial, credential, communication, and execution boundaries.
- A local Ollama/Qwen3 8B agent for lightweight tasks.
- A cloud-model fallback.
- MiniMax was previously configured as a primary model.
- Skills for content generation, scheduling, documentation, and other procedures.
- Git-backed configuration and cross-machine knowledge repositories.

However, a July 2026 portfolio audit found that much of this AI infrastructure became dormant because the workflows it supported stopped producing regular output. It specifically identified a pattern of building sophisticated tools and documentation but delaying the recurring operational step that generates value.

Examples included:

- Building financial analysis tools but not maintaining current input data.
- Building health tracking but not maintaining the recurring logging cadence.
- Building content systems but not consistently publishing.
- Building gaming analytics while higher-risk operational and measurement tasks remained open.
- Building OpenClaw and resource-indexing infrastructure before proving a sustained workload for them.

This audit's core conclusion was that recurring, unglamorous operational tasks are the real automation opportunity.

## Recent automation design work

I recently used Grok, Claude, Codex, and Kimi to design a vendor-neutral system for sending AI CLI status notifications to Discord.

The process produced:

- A detailed architecture prompt.
- A Grok architecture response.
- An independent review that found unverified vendor-hook claims and design gaps.
- A corrected implementation plan for Codex.
- Kimi-specific feedback.

The current design recommends a PowerShell notifier, file-backed queue, generic process wrapper, and optional vendor adapters. It has not yet been demonstrated to improve the completion of a real workflow. Treat it as a candidate capability, not automatically as a priority.

## My uncertainty

I am considering uninstalling OpenClaw from the Mac Mini and installing Hermes Agent. This idea currently comes mainly from social-media exposure, not a clear workload requirement.

I also wonder whether the Mac Mini could run a local model as a "workforce bot." However, much of my recent architecture, debugging, code review, and research has required leading-edge cloud models. I do not want to force difficult work onto a weaker local model merely to avoid token costs.

Hermes Agent currently advertises skills, memory, messaging, cron, local/cloud model routing, auxiliary models, security controls, and self-improvement features. Its documentation says agentic local models need at least a 64K context window. Verify these claims and assess their practical implications for an M4 Pro with 24 GB unified memory.

Relevant official starting points:

- Hermes Agent documentation: https://hermes-agent.nousresearch.com/docs/
- Hermes local/provider documentation: https://hermes-agent.nousresearch.com/docs/integrations/providers/
- Hermes security documentation: https://hermes-agent.nousresearch.com/docs/user-guide/security/
- OpenClaw repository/documentation: https://github.com/openclaw/openclaw

Do not limit research to these pages, but prefer official documentation and repositories.

## Tasks

1. Diagnose my current working style.

Identify:

- What is already working well.
- Where multiple-model review genuinely improves quality.
- Where it creates ceremony, duplicated analysis, or delayed implementation.
- Where stale `HANDOFF.md`, `_TODO.md`, audit documents, or dirty repositories indicate context-maintenance problems.
- Whether I am over-investing in agent infrastructure relative to recurring output.

2. Separate my workloads into five execution tiers:

- Deterministic automation requiring no LLM.
- Small local-model work.
- Cheap cloud-model work.
- Frontier-model work using Claude, Codex, Grok, Kimi, or similar.
- Human-only decisions or approval gates.

For each candidate workload, state why it belongs in that tier. Do not recommend a local LLM for tasks where weaker reasoning would materially increase risk or rework.

3. Build a three-machine responsibility model.

Recommend what should run on:

- Development Windows workstation.
- Gaming Windows workstation.
- Mac Mini M4 Pro with 24 GB.
- Cloud frontier models.

Account for Git synchronization, VS Code workflows, always-on services, secrets, backups, failure recovery, remote access, and avoiding two machines modifying the same working tree concurrently.

Do not assume the Windows machines' hardware specifications. State what additional hardware facts would change the design.

4. Evaluate these Mac Mini options:

- Keep and simplify OpenClaw.
- Keep OpenClaw but change its workloads or model routing.
- Install Hermes alongside OpenClaw in an isolated pilot.
- Migrate from OpenClaw to Hermes.
- Remove both and use ordinary scripts, scheduled tasks, and frontier CLIs.
- Use Hermes or OpenClaw only as an orchestration shell while routing difficult tasks to frontier models.

Compare:

- Proven useful capabilities.
- Existing migration investment.
- Compatibility with my current skills and memory files.
- Security boundaries.
- Local-model support.
- Cloud/frontier-model routing.
- Cron and event-driven automation.
- Messaging.
- Observability and auditability.
- Backup and rollback.
- Maintenance burden.
- Risk of prompt injection or unintended execution.
- Likelihood that the framework improves actual output.

Give an explicit recommendation. Do not recommend uninstalling OpenClaw merely because Hermes is newer.

5. Assess realistic local-model use on the M4 Pro with 24 GB.

Research and explain:

- Realistic model-size and quantization ranges.
- The memory impact of a 64K context window and KV cache.
- Expected performance for tool calling, summarization, classification, document triage, coding, and multi-step autonomous work.
- Which local workloads would be dependable enough for unattended use.
- Which workloads should always escalate to a frontier model.
- Whether Ollama, MLX, llama.cpp, or another runtime is the most practical fit.
- Whether running an agent framework and local inference together leaves enough memory headroom.
- How to benchmark this on my actual machine instead of relying on generic benchmark tables.

Do not invent exact tokens-per-second figures. Cite current hardware/model benchmarks only when they match the M4 Pro and relevant memory configuration.

6. Identify and rank concrete automation candidates from my actual portfolio.

Consider at least:

- Git status, stale branch, failed test, backup, and stale-HANDOFF monitoring.
- A weekly cross-project operational review.
- Documentation intake, indexing, classification, and duplicate detection.
- Draft preparation and fact extraction from approved documents.
- Read-only financial-data freshness checks and report preparation.
- Read-only gaming P&L and operational-health reporting.
- Health-tracking reminders and summaries without medical decision-making.
- ControlsBMW backlog review, schedule auditing, and draft preparation without autonomous posting.
- CLI task completion and approval notifications.
- Converting repeated AI procedures into tested scripts or skills.
- Detecting when an audit/review chain is producing documents without moving an operational metric.

Rank each by:

- Expected value.
- Frequency.
- Implementation effort.
- Reliability.
- Privacy sensitivity.
- Consequence of error.
- Best execution tier.
- Best machine.
- Whether it requires an LLM at all.
- Measurable success criterion.

7. Design a hybrid escalation architecture.

Show how a task should flow through:

event or schedule -> deterministic pre-check -> local model if appropriate -> frontier model escalation if needed -> human approval -> action -> audit log

Include:

- Clear escalation triggers.
- Per-task model pinning.
- Cost and token controls.
- Timeouts and bounded retries.
- Idempotency and duplicate prevention.
- No recursive agent scheduling.
- A global kill switch.
- Read-only defaults.
- Logs that record what model made what decision.
- Safe handling of employer, health, financial, wallet, and credential-related data.
- A rule preventing external documents from becoming executable instructions.

Provide a Mermaid diagram.

8. Propose a reversible 30-day pilot.

The pilot MUST:

- Avoid uninstalling OpenClaw initially.
- Select no more than three recurring workflows.
- Include at least one deterministic/no-LLM workflow.
- Include at most one local-LLM workflow.
- Use a frontier model only where the task justifies it.
- Run Hermes only in an isolated environment if it is part of the pilot.
- Avoid autonomous financial transactions, medical decisions, public posts, arbitrary shell execution, or messages to third parties.
- Establish baseline time and completion rates before automation.
- Define pass/fail metrics.
- Define rollback and cleanup.
- Include a decision gate for keep OpenClaw, migrate to Hermes, keep neither, or continue the comparison.

9. Improve my multi-model interaction process.

Design a lighter protocol for deciding:

- When one frontier model is enough.
- When an independent reviewer is justified.
- When vendor-specific review is justified.
- When a written execution plan is necessary.
- When the next action should be implementation instead of another audit.
- How to stop circular model-to-model review.
- How to preserve useful context without maintaining redundant documentation.

Include a compact decision tree I can use before starting a new AI session.

## Safety constraints

- Do not recommend autonomous trades, purchases, wallet operations, or financial transfers.
- Do not recommend autonomous medical decisions.
- Do not recommend sending email, messages, or public posts without explicit human approval.
- Do not expose or centralize secrets in repositories or prompts.
- Do not recommend arbitrary remote shell control through Discord.
- Do not recommend uploading private employer, health, financial, or wallet data to an external model.
- Prefer read-only monitoring, draft generation, summaries, and approval-gated actions.
- Do not propose a multi-agent system merely to organize skills.
- Do not equate "local" with "safe"; consider prompt injection, filesystem access, and unattended execution.
- Do not propose Kubernetes, a vector database, an MCP server, or another persistent service unless it solves a demonstrated requirement better than a simple script or existing framework.
- Do not write implementation code or modify files. This is an evidence-based assessment and decision plan.

## Required output

1. Executive verdict in no more than 250 words.
2. Evidence-based assessment of my current workflow.
3. Current-state diagram.
4. Workload-routing matrix across the five execution tiers.
5. Three-machine responsibility matrix.
6. OpenClaw versus Hermes versus neither decision matrix.
7. M4 Pro 24 GB local-model feasibility assessment.
8. Ranked automation backlog with no more than 12 candidates.
9. Recommended hybrid escalation architecture and Mermaid diagram.
10. Thirty-day pilot with weekly stages, metrics, stop conditions, and rollback.
11. Simplified multi-model review protocol and decision tree.
12. Final recommendation containing:
    - What to keep.
    - What to stop doing.
    - What to test first.
    - What not to install yet.
    - The first three actions I should take next week.
13. A short list of missing information that would materially change the recommendation.

For every major recommendation, label it as one of:

- Verified fact.
- Inference from my workspace evidence.
- Conditional recommendation.
- Unknown requiring measurement.

Use concrete language and measurable criteria. Challenge my assumptions when the evidence supports doing so. The goal is not to build an impressive AI stack. The goal is to complete more valuable recurring work with less supervision and less duplicated model effort.
```

**Target:** Grok  
**Optimization:** Evidence-based workspace architecture, hybrid local/frontier model routing, and a reversible OpenClaw-versus-Hermes decision instead of a trend-driven migration.

## Before using

Attach only the non-sensitive workspace summaries and `_audits` documents you want Grok to inspect. Do not upload employer exports, health records, financial data, credentials, or wallet information.
