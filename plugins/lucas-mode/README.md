# Lucas Mode

A skills-only plugin for focused engineering work and direct behavioral proof.

## Skills

- `lucas-mode` selects a proportionate engineering workflow, makes focused
  changes, and verifies the affected behavior.
- `verify-work` tests a falsifiable claim against the actual artifact and reports
  VERIFIED, NOT VERIFIED, or INCONCLUSIVE.
- `project-verification` creates or maintains a repository verification skill and
  feature map, with launch, doctor, drive, evidence, and owned cleanup.

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

- `lucas-mode`: pstack's [poteto-mode](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/poteto-mode).
- `verify-work`: pstack's [prove-it-works](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/principle-prove-it-works) and Cursor Team Kit's [verify-this](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/cursor-team-kit/skills/verify-this).
- `project-verification`: pstack's [create-verification-skill](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/create-verification-skill) and [maintain-verification-skill](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/maintain-verification-skill).

Copyright and MIT notices remain in each skill's `LICENSE` file so they travel
with copied skill folders.
