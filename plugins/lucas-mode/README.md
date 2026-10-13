# Lucas Mode

A skills-only plugin for focused engineering work and direct behavioral proof.
It has no MCP server, startup hooks, credentials, or model overrides.

## Skills

- `lucas-mode` selects a proportionate engineering workflow. It adapts pstack's
  **poteto-mode**, which is a rigorous work style rather than a low-token mode.
- `verify-work` tests a falsifiable claim against the actual artifact and reports
  VERIFIED, NOT VERIFIED, or INCONCLUSIVE.
- `project-verification` creates or maintains a repository verification skill and
  feature map, with launch, doctor, drive, evidence, and owned cleanup.

The skills preserve repository checks and current authorization. They do not
grant permission to merge, deploy, send messages, execute unrecognized software,
or change runtime settings. Upstream sources and MIT notices accompany the skills.

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
