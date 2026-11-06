# Correctness and reliability audit — 2026-11-06

## Baseline and inventory (recorded before implementation)

Remote default `896abe2c5d2e51042e26e703ef21987f46e054bb` includes the merged
untangle pass (#22). The isolated worktree was clean and at that commit.

- Public interfaces: portable marketplace/plugin/MCP JSON, skill frontmatter,
  generated Claude/Cursor catalogs and manifests, `python scripts/sync.py [--check]`.
- Source/data flow: maintained JSON and skill files → validation → artifact map →
  byte comparison or writes. Python standard-library json/pathlib/urllib/argparse
  already cover parsing and CLI needs. No dependencies are needed.
- Persistence: tracked generated files; no database or production writes.
- Trust boundaries: repository-relative input paths and output filesystem paths;
  remote MCP URLs are configuration, never contacted by the generator.
- Five plugins expose remote services and instructions. Authentication, tenant
  isolation, retries, request cancellation and transactions belong to those
  separate service repositories. Skills do not implement those mechanisms.
- CI runs artifact validation and Python unittest subprocess journeys covering
  validation, no-write failures, drift detection and regeneration. Dependabot
  merging checks same-repository actor/head SHA and uses match-head-commit.
- No JavaScript/TypeScript source, package manifest, web/native application or
  JavaScript subproject exists. The requested tester-army `e2e` package and
  @e2e-dev/web/mobile have no applicable target here; no unrelated UI or npm
  dependency is introduced. Python CLI journeys remain the end-to-end coverage.

## Confirmed findings

1. **Medium / high confidence: removed MCP sources leave live generated servers.**
   `build_artifacts` omits `.mcp.json` when portable `mcp.json` is absent, while
   `check_artifacts` only checks present map entries and sync only writes them.
   Trigger: remove `plugins/travel/mcp.json`, then check/sync. Actual: check can
   succeed and Claude still loads the old server. Expected: check reports stale
   connection metadata and sync removes that generator-owned mirror. Scope is
   registered plugins only; unrelated files must never be deleted.
2. **Medium / high confidence: generated symlinks bypass write confinement.**
   `main` confines plugin source directories, but `save` follows output-file and
   output-parent symlinks. Trigger: link `.cursor-plugin/marketplace.json` or its
   parent to an external sentinel/directory, then sync. Actual: external bytes
   are overwritten after some outputs may already be written. Expected: fail
   before any mutation, with an actionable diagnostic. Check must also reject
   this unsafe destination rather than read outside the checkout.

## Reconciled and rejected hypotheses / limits

- Validation errors are accumulated before generation: malformed manifests,
  invalid URL ports, duplicate names and source `..` traversal already fail.
- Generated malformed JSON is compared as bytes and can be repaired; no need to
  reintroduce parsing of generated files from the old structural design.
- Current remote URLs and hosted service semantics cannot be proved by local
  metadata; no live credentials or production calls are used.
- Concurrent hostile filesystem replacement and all-or-nothing recovery from
  disk/power failure are not promised by this developer CLI. Output preflight
  handles stable unsafe paths; it is not an OS sandbox or transactional storage.
- Skill instructions defer to current connected tool schemas; no concrete
  instruction/API mismatch established. No speculative skill rewrites.

## Validation plan

Add contract tests for removal/check/repair/idempotency and external symlink
sentinels/no-write failure. Run only in CI. A dedicated CI job substitutes the
baseline generator and requires each regression to fail with its specific
assertion, establishing pre-fix behavior independently of the fix. Preserve all
existing checks. Independent reviewer challenges findings and implementation.

## Evidence and outcome

Pending implementation, independent review and CI; no local tests or builds run.

Framework sources inspected: [upstream](https://github.com/tester-army/e2e),
[quickstart](https://e2e.com/docs/quickstart.md),
[CI](https://e2e.com/docs/ci.md), and
[GitHub Actions](https://e2e.com/docs/ci/github-actions.md). They document browser
and mobile engines and credential-free deterministic tests. No such target is
present in this Python/metadata repository. No package installation was needed.

Independent static review confirmed both defects and requested strengthening the
symlink regression with an earlier stale output: that output must stay stale on
failure, detecting partial writes even when they would otherwise be idempotent.
This objection was addressed before submission. No local tests/builds run.
