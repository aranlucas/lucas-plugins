# Lucas Mode

A skills-only adaptation of poteto-mode for engineering work coordinated through
T3 Code or the host's native agents.

## Skills

- `lucas-mode` routes work through 24 playbooks and 24 engineering principles.
  It coordinates research, competing designs, implementation, independent review,
  and behavioral verification.
- `verify-work` tests a falsifiable claim against the actual artifact and reports
  VERIFIED, NOT VERIFIED, or INCONCLUSIVE.
- `project-verification` creates or maintains a repository verification skill and
  feature map, with launch, doctor, drive, evidence, and owned cleanup.

## Orchestration

The coordinator owns the outcome and assigns bounded work to other agents.
The [T3 adapter](skills/lucas-mode/references/t3-orchestration.md) uses the live
provider/model catalog, native subagents where they support the selected model,
and T3 `delegate_task` for cross-provider work or T3-owned children. It covers
complete briefs, async completion, fresh review rounds, cancellation, exclusive
write ownership, and recovery from partial results.

[Agent workflows](skills/lucas-mode/references/agent-workflows.md) preserve the
upstream Ground, Architect/Arena, Swarm, and independent-review patterns. The
[Orchestrate playbook](skills/lucas-mode/playbooks/orchestrate.md) adds a durable
task ledger and rolling dispatch for larger programs. Read supporting files only
for the selected workflow.

T3-owned delegation requires a running parent thread inside T3. Merely exposing
the MCP tools to another host does not create that parent. Outside T3, the skill
uses available native delegation and reports any missing orchestration capability.

## Install and invoke

For Claude Code, install `lucas-mode@lucas-plugins` from this marketplace. For
Cursor, enable Lucas Mode after importing `aranlucas/lucas-plugins`. Other Agent
Plugins clients can use this standalone plugin directory.

For T3 Code, discovery belongs to the selected provider. The repository's
generated `.agents/skills` files and relative `.claude/skills` links expose these skills when this checkout
is the workspace. Invoke `$lucas-mode`, `$verify-work`, or `$project-verification`
from the skill picker. This does not install them in other projects or globally.
Plugin-installed clients may expose namespaced names; use the name their picker
actually returns.

To use them in another Codex project, copy the three sibling skill folders into
that project's `.agents/skills`, preserving their names, references, and licenses.
For Claude, use the project's `.claude/skills` convention. Preserve any conflicting
entry and inspect its purpose before replacing it. See the
[T3 reference](skills/lucas-mode/references/t3.md) for paths and provider limits.

Validate this package with the root repository's sync and unittest commands.
Markdown validation and dispatch checks establish packaging and routing only;
a live T3 behavior claim needs an invocation against the intended provider,
profile, and workspace.

## Attribution

These skills adapt the following MIT-licensed workflows from
[`cursor/plugins` at `fe53d9e`](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08):

- `lucas-mode`: pstack's [poteto-mode and playbooks](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/poteto-mode), its 24 principle skills, and the supporting `how`, `architect`, `arena`, `swarm`, `interrogate`, `figure-it-out`, `show-me-your-work`, and `benchmark-checklist` workflows.
- `verify-work`: pstack's [prove-it-works](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/principle-prove-it-works) and Cursor Team Kit's [verify-this](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/cursor-team-kit/skills/verify-this).
- `project-verification`: pstack's [create-verification-skill](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/create-verification-skill) and [maintain-verification-skill](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/maintain-verification-skill).

Copyright and MIT notices remain in each skill's `LICENSE` file so they travel
with copied skill folders.

The [pstack-claude port](https://github.com/michael-denyer/pstack-claude/tree/058a34816dd7dc61e0a8221c7099bc64364a2577)
was also consulted for cross-runtime adaptation and review lifecycle behavior.
The principles retain upstream guidance; the playbooks adapt runtime-dependent
operations to T3. Cursor model slugs, cloud placement, watcher scripts, and local
transcript assumptions are replaced by live capabilities and task IDs. Supporting
agent workflows are bundled as references, so the package does not require the
rest of pstack to be installed.
