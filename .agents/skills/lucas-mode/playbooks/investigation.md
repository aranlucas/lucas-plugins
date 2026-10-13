# Investigation

**You own the answer. Plan, route, write.**

Investigation requests are read-only. They produce a cited explanation or a recommendation, not a code change.

1. Route through the [Ground](../references/agent-workflows.md#ground) workflow. For motivation questions, also route through the [Ground and rationale](../references/agent-workflows.md#ground) workflow.
2. Throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only investigation`.
3. Produce the [Ground](../references/agent-workflows.md#ground)-shaped output (Overview / Key Concepts / How It Works / Where Things Live / Gotchas), or a recommendation with a tradeoffs table if the request is a decision between alternatives.
4. Follow Lucas Mode's communication guidance: direct prose, relevant evidence, and explicit uncertainty.

No PR, no babysit, no [Architect](../references/agent-workflows.md#architect-and-arena) unless the investigation precedes a code change. If implementation was also requested, continue with Bug fix or Feature after the investigation.

**Reply:** the investigation output. For "are we sure?" answers, include your real judgment with reasons. Push back if the premise is wrong (see Lucas Mode's execution guidance).
