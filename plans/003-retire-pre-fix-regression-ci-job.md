# Plan 003: CI keeps only checks worth maintaining (retire the pinned pre-fix reproduction job)

> **Executor instructions**: Follow the steps, run each verification, honor the
> STOP conditions, update `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 8b8f81e..HEAD -- .github/workflows/ci.yml tests/test_sync.py`

## Status

- **Priority**: P3
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx
- **Planned at**: commit `8b8f81e`, 2026-11-11

## Why this matters

`.github/workflows/ci.yml:40-77` (`regression-baseline`) runs on every push and PR.
It overwrites `scripts/sync.py` with the copy from commit `896abe2`, then requires
two named tests to *fail*. That proved the #23 fixes once. It is
temporary development scaffolding, which `AGENTS.md` says to keep apart from
checks worth maintaining ("Distinguish temporary development scaffolding from
checks worth maintaining"). It also couples CI to test names and fixture paths
(`plugins/travel`, `.cursor-plugin/`). A routine test rename or a fixture change
breaks it without any regression. On every run it also uploads artifacts
(`actions/upload-artifact`) that nobody consumes.

## Current state

- `ci.yml:16-38`: job `ci` runs `python scripts/sync.py --check` and the unittest suite. Keep it.
- `ci.yml:40-77`: job `regression-baseline`, a matrix of
  `test_removed_mcp_source_removes_generated_connection` and
  `test_generated_symlinks_cannot_overwrite_external_files`.

## Scope

In: `.github/workflows/ci.yml` only. Out: the two tests (they stay, and they guard the fixes).

## Steps

1. Delete the `regression-baseline` job (lines 40-77). Leave `ci` untouched.
   **Verify**: `python3 -c "import yaml"` may be unavailable. Instead,
   `grep -c 'regression-baseline' .github/workflows/ci.yml` → `0`, and
   `grep -n 'sync.py --check' .github/workflows/ci.yml` still matches.
2. Run the suite locally: the unittest command → `OK`.

## Done criteria

- [ ] `grep -c 896abe2 .github/workflows/ci.yml` → `0`
- [ ] Both named tests still exist: `grep -c 'def test_removed_mcp_source_removes_generated_connection\|def test_generated_symlinks_cannot_overwrite_external_files' tests/test_sync.py` → `2`

## STOP conditions

- If the owner records that the reproduction job is meant to be permanent,
  mark this plan REJECTED.

## Maintenance notes

If proof of a pre-fix failure is wanted for a future fix, record it in the PR
body (as #23 did in `docs/reliability-audit.md`) instead of adding a permanent CI job.
