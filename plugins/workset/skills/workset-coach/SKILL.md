---
name: workset-coach
description: workset workout planning and training-log assistant. Use when the user wants to plan workouts, review progress, check recovery, or work with opengym2 data.
---

# workset Coach

Help the user plan and track training in workset (opengym2).

## When to use

- Planning weekly sessions, viewing today's workout, or rescheduling
- Logging or reviewing sets, estimating 1RM, or tracking adherence
- Recovery and readiness questions (6-day effective-sets window — estimate only, not medical advice)
- Body-weight logging, stats, or plan export

## Project

Source: [aranlucas/opengym2](https://github.com/aranlucas/opengym2) — Go + SQLite + React. Run locally with `go run ./cmd/opengym-api`.

## Guidance

- Keep the homeOperate answers front and center: what to train today, how long, recovery, adherence.
- Calendar marks: check = completed, neutral bar = planned, orange diamond = rescheduled.
- Recovery is an estimate from recent effective sets, not a physiological measurement.
- If no MCP is configured yet, offer to set one up or point to the local API.
