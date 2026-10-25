# AP2 (Agent Payments Protocol) — evidence packet

Home layer: L4. Origin in corpus: web2 (`spec-ap2`); blog describes hybrid rails.

## Canonical locators

- `spec-ap2` https://github.com/google-agentic-commerce/AP2
- `ind-google-ap2-blog` https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol (2025-09-17)
- `ind-digitalapplied-standards` AP2 creates signed payment mandates as W3C Verifiable Credentials
- `ind-crossmint-compare` AP2 is a trust and authorization layer using cryptographically signed mandates
- UCP spec binds payment to AP2: https://ucp.dev (AP2 mandates and VCs)

## Documented artifacts

From the Google announcement:

- Intent Mandate and Cart Mandate: tamper-proof cryptographically signed digital contracts, signed as verifiable credentials.
- Human-present: Intent Mandate then Cart Mandate on approval; “what you see is what you pay”.
- Human-absent: detailed Intent Mandate with price, timing, conditions; agent may generate Cart Mandate when conditions match.
- Chain of evidence: intent → cart → payment method, described as a non-repudiable audit trail for authorization and authenticity.
- Payment-agnostic: cards, stablecoins, real-time bank transfers.
- A2A x402 extension (with Coinbase, Ethereum Foundation, MetaMask) for agent crypto payments.
- 60+ named industry collaborators; public GitHub spec and reference implementations.
- Positions itself as an extension of A2A and MCP.

Corpus `spec-ap2` synopsis is thinner (repo of samples, human-present card payments, env-var credentials) than the blog. Prefer the blog + UCP binding for mandate claims.

## Failures named in sources

- Blog lists the problems AP2 claims to solve: proving specific authority, merchant certainty of intent, accountability after fraud or error. It does not specify an agent-speed dispute forum or a delivery-proof bind.
- Ledger T2: a valid L4 signature does not prove correct L3 behavior.
- Ledger L4 open issue: revocation not consistently propagated into settlement.
- `arxiv-2511.03434v1` discusses A2A, AP2, ERC-8004 trust models; receipts and logs are not themselves remedy.

## What is not in the packet

No independent production reliability numbers. No human-coded κ. No measurement of revocation latency or scope-violation rate in the wild.
