---
name: travel-planner
description: Plan trips using trvl to search flights, hotels, ground transport, rental cars, and destinations. Use for travel research, itinerary planning, and comparing trip options.
---

# Travel Planner

Use the connected `trvl` MCP server and its current tool schemas for travel
searches. If the server is unavailable, report the connection issue rather than
asking the user to install a local CLI. For authentication failures, check that
`TRVL_MCP_TOKEN` is available to the MCP client; never ask the user to paste the
token into chat.

## Workflow

1. Reuse the user's stated origin, destination, dates, traveler count, budget,
   currency, and preferences. Ask only for missing details needed for the search.
2. Search the relevant transport and accommodation tools. For flexible trips,
   compare nearby dates or airports when those options suit the user's constraints.
3. Compare total costs, baggage, transfers, travel time, overnight connections,
   cancellation terms, and accommodation location when the source provides them.
   Identify missing fees and unavailable information explicitly.
4. Present a short ranked set of options with source or booking links returned
   by the tools, dates, currency, and the reason each option fits.
5. Build a feasible itinerary around the selected options, including transfer
   time and check-in constraints. Recheck availability before a booking decision.

## Accuracy and actions

- Treat prices and availability as search-time observations, not guarantees.
- Report provider failures or missing credentials; do not invent live results.
- Keep estimates separate from quoted prices and preserve the source currency.
- Use current official sources for entry requirements when relevant.
- Do not book, purchase, send messages, or change saved traveler preferences
  unless the user has authorized that action.
- Do not scan email or calendars to build a profile unless the user requests it.
