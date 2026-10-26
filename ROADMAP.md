# Lucas Plugins feature roadmap

Updated 2026-10-26. Proposed sequence, not delivery dates. Success targets below are unvalidated pilot gates, not adoption or revenue results.

## User and current baseline

A user wants to install the right MCP capability in their client, connect their account and complete a first useful task without troubleshooting manifests.

The marketplace already packages groceries, workset, Shipshape, travel and System Design connections with client manifests and optional skills. It distributes integrations; it should not become a second service runtime.

Planning source: [README](README.md) at `9d27197a9e41`. This is a focused planning pass, not a new comprehensive code audit or live-service validation.

## Prioritized releases

| Order | Feature                                             | Useful scope                                                                                                                               | Release acceptance                                                                                                                             |
| ----- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Now   | A first-use guide for each supported client         | Give each plugin one concise install/connect/first-task journey and state which host capabilities are required.                            | A new user in each explicitly supported client reaches one useful result; unsupported host behavior is labeled rather than implied compatible. |
| Next  | Repair a connection without reinstalling everything | Provide service-specific reconnect instructions and a small set of actionable states: not installed, not authorized, unavailable or ready. | A user can repair one plugin without losing another plugin’s configuration or exposing a credential.                                           |
| Next  | Choose by outcome, not tool inventory               | Present a few concrete workflows and their boundaries, linking to the underlying product roadmap and account permissions.                  | A user can select a plugin for their task and understand which actions still require explicit approval.                                        |
| Later | Predictable updates and compatibility               | Publish concise per-plugin change notes and a tested host/service compatibility record using existing manifest tooling.                    | An upgrade identifies changed permissions or contracts and provides a recoverable path when a host is unsupported.                             |

## Measure before expanding

Baseline five installs/connects across the intended clients: time to first useful tool result, setup failures and support requests. Proposed first gate: four succeed without manual manifest editing. Count repeat successful workflows, not the number of bundled tools.

Collect the baseline before implementation. Use voluntary feedback and aggregate operational events without private content, credentials or account identifiers. If users do not return to the first workflow, revisit it before adding the later milestones.

## Dependencies and limits

Runtime features belong to their service repositories. Skills must describe the actual service contract and should not silently expand authorization. Add Digits or Garmin distribution only after their first-use journey and target-client support are verified.

Use existing libraries and native test commands. Attach reliability work to the feature acceptance it enables. Update this file with shipped user outcomes and observed pilot results; refactors or passing tests alone do not demonstrate product value.
