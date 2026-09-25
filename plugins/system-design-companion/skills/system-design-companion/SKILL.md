---
name: system-design-companion
description: Collaborate on a System Design Companion canvas. Use when the user wants to create or edit architecture diagrams, join a shared system design session, or review a design on the canvas.
---

# System Design Companion

Use the connected System Design Companion MCP tools to work on the shared canvas.

1. Use the user's diagram share link, or create a diagram when requested. Join the
   session once and retain the same link for subsequent diagram operations.
2. Read the scene before editing. When the user refers to “this” or “these,” check
   the current selection. Inspect a screenshot when visual layout matters.
3. Batch related edits with `apply_patch`. Prefer standard component kinds,
   placement hints, and frames. Include a short summary of the requested change.
4. Keep labels concise and put longer explanations in notes. Use `tidy` to improve
   readability; use `layout` when the user asks to rearrange the diagram.
5. Deliver design feedback in chat. Add review notes to the canvas when requested.

Follow the server's current tool schemas and session instructions. Do not invent
component IDs or diagram links; obtain them from the user or tool results.
