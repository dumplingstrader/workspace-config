# How to Prompt GPT-5.6

Five habits from OpenAI's own docs that make the biggest difference.

---

## 1. Trim your prompt

Leaner system prompts improved eval scores by **10–15%** while cutting tokens
**41–66%** in OpenAI's own tests. State each instruction once, and only expose
the tools the task needs.

> "State each instruction once; expose only the tools the task needs."

## 2. Set autonomy once, not repeatedly

Define what it can do without asking, and what needs approval. Repeating “ask
first” or “don't mutate” causes unnecessary pauses on safe, expected actions.

> "For change/build requests: make in-scope local changes and validate without
> asking first. Require confirmation for external writes, destructive actions,
> or scope expansion."

## 3. Say what to keep, not just “be short”

GPT-5.6 is already more concise by default. If you need brevity, specify what
must survive the cut.

> "Lead with the conclusion. Include the evidence needed, any caveat, and the
> next action. Omit secondary detail."

## 4. Match reasoning effort to the task

**Medium** is the balanced default. Move to **high/xHigh** only when more
reasoning shows a real quality gain, and reserve **max** for the hardest,
quality-first work.

## 5. Reach for Pro mode selectively

Use the same prompt as standard mode; there is no need to say “think harder.”
Use Pro mode when a marginal quality gain genuinely matters, and skip it for
routine or latency-sensitive work.

---

> **Underneath it all:** GPT-5.6 infers your intent and effort level better than
> prior models. You still need to state context, hard constraints, approval
> boundaries, and success criteria explicitly.

Source: OpenAI Developer Docs — *Using GPT-5.6*
