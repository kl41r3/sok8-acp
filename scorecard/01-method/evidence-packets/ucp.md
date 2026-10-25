# UCP (Universal Commerce Protocol) — evidence packet

Home layer: L6 (also L1/L2/L4/L5 in corpus tags). Origin: web2 (`spec-ucp`); site claims hybrid MoR + AP2.

## Canonical locators

- `spec-ucp` and `protocol-root-universal-commerce-protocol` https://ucp.dev
- Official spec https://ucp.dev/latest/specification/overview/
- Checkout / order examples on https://ucp.dev (checkout sessions, fulfillment events, refund adjustments)
- GitHub https://github.com/Universal-Commerce-Protocol/ucp
- `ind-digitalapplied-standards` UCP covers discovery and cart; ACP checkout; AP2 mandates
- `ind-agenticplug-tracker` UCP cart, catalog, identity linking

## Documented artifacts

- `/.well-known/ucp` business profile: versioned services, capabilities, payment handlers, signing keys.
- Capabilities: catalog, cart, checkout, fulfillment, identity linking (OAuth 2.0), order webhooks, refund adjustments.
- Transports: REST, MCP, A2A (Agent Card URL), embedded.
- Built-in support for AP2, A2A, MCP. Payment via AP2 mandates and VCs; businesses remain Merchant of Record.
- Order object: fulfillment events (`delivered`), tracking, `adjustments` type `refund`.
- Negotiation: capability intersection, version dates (YYYY-MM-DD), `continue_url` fallback to merchant web checkout.
- Co-developed / endorsed by large retail, lodging, food, and payment firms (Google, Shopify, Walmart, Stripe, Visa, etc.).
- Lodging and food verticals: “detailed specifications coming soon” (site).

## Failures named in sources

- Ledger L6: post-purchase state and refund portability remain merchant-specific (T4). UCP specifies order/refund objects, but portability depends on merchant implementation of webhooks and handlers.
- Payment architecture: platform SHOULD NOT touch raw credentials; completion still goes through the business and its PSP. Economic finality is PSP/card/bank, not UCP itself.
- `continue_url` is graceful degradation to the web storefront, not an L8 forum.
- No native agent-speed dispute protocol in the fetched spec overview.
- Corpus n for L6 is 36, thinnest interim layer.

## What is not in the packet

No independent count of production UCP checkouts. Lodging/food specs incomplete on the site.
