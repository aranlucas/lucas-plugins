---
name: shopping-assistant
description: Kroger/QFC grocery shopping — search products, manage shopping lists and cart, track pantry and weekly deals. Use when the user wants to shop, plan meals, or manage groceries.
---

# Shopping Assistant

Help the user shop at Kroger/QFC via the connected MCP.

## Tools available (via MCP `groceries`)

- Discovery: `search_stores`, `get_store`, `set_preferred_store`
- Search: `search_products` (1–10 terms in parallel), `get_product`
- Shopping: `shop_for_items` (one-shot search + list), `create_shopping_list`, `add_shopping_list_to_cart`, `view_cart`
- Pantry/kitchen: `add_to_inventory`, `remove_from_inventory`, `get_shopping_profile`
- Orders/deals: `record_order`, `get_weekly_deals`, `get_meal_planning_context`

## Golden path

1. `shop_for_items` with item names (or `search_products` → `create_shopping_list`)
2. `add_shopping_list_to_cart` with the returned `listId`
3. `view_cart` to confirm

Use `get_shopping_profile` before personalized suggestions. For pantry-aware flows, check inventory first. For savings, call `get_weekly_deals`.

## Response format

MCP text responses include `key=value` ids (`storeId=...`, `upc=...`, `listId=...`) — extract with regex, no JSON parsing needed. Error text names the recovery tool to call next.
