# Repository Structure Audit

Reviewed September 7, 2026. Scope: repository layout, catalog registration,
manifest generation, validation, tests, and CI. This is not a live client
installation or remote MCP service audit.

## Findings

- **P2: Generated Cursor manifests are also configuration inputs.**
  **Resolved October 2, 2026:** custom `displayName` values now live in optional
  maintained `plugins/*/cursor.json` files. `scripts/sync.py` validates this
  metadata without reading generated Cursor manifests, so deletion or corruption
  of those outputs can be repaired and `--check` detects display-name drift.
- **P2: License metadata is inconsistent.** `plugins/groceries/plugin.json`
  and `plugins/workset/plugin.json` declare ISC, while the root `LICENSE` is MIT
  and neither plugin includes an ISC license file. Clarify whether the metadata
  describes this plugin package or its upstream service, then align the package
  declarations and license text. This audit preserves the existing declarations.
- **P3: Validation is a targeted check, not full schema validation.** The sync
  script checks selected fields but does not load the referenced schemas. For
  example, malformed marketplace metadata can still raise an exception instead
  of producing a validation diagnostic. Add explicit shape checks or pinned
  schema validation if accepting third-party plugin contributions.

## Repairs Included

- Tests discover plugin names from the catalog, so travel and future plugins
  participate in artifact, MCP mirror, and skill-path checks.
- Validation rejects invalid stdio commands and arguments, version drift between
  the catalog and manifest, missing Cursor logos, skill directories without
  `SKILL.md`, and plugin manifests not registered in the catalog.
- The development instructions now show generation before the freshness check
  and document maintained files, generated files, and the test command.

## Layout Assessment

The small `plugins/<name>` packages and shared generator are appropriate for
this collection. Client-specific catalogs have different path conventions, so
their separate generated files are intentional. A package manager, build
framework, or service source code is not needed here. Keep server implementations
in their upstream repositories and keep this repository focused on distribution
metadata, skills, assets, and validation.
