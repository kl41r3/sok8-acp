# MCP (Model Context Protocol) — evidence packet

Home layer: L2 / L3. Origin: web2 (`protocol-root-model-context-protocol`).

## Canonical locators

- `protocol-root-model-context-protocol` https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro
- `sur-ehtesham2025-agent-interop` https://arxiv.org/pdf/2505.02279 survey of MCP, ACP, A2A, ANP
- `oa-w4415947096` measurement study of the MCP ecosystem
- A2A site: MCP = agent-to-tool; A2A = agent-to-agent
- AG-UI docs: same three-layer split
- UCP: MCP is a first-class transport

## Documented artifacts

- Open standard for connecting AI apps to tools, data sources, and workflows (USB-C metaphor).
- Clients: Claude, ChatGPT, VS Code, Cursor, and others listed on the intro page.
- Server/client/apps build paths; versioned docs dated 2026-07-28.
- Capability discovery: prompts, resources, tools, completions (also stated in ERC-8004 Motivation).
- User-mediated delegated access (`protocol-root` trust_model).
- Broad independent implementations (the strongest maturity signal in this set).

## Failures named in sources

- Ledger L2: advertised capability is not bound to demonstrated competence.
- Ledger L3: tool-call logs exist; completion ≠ fidelity to principal intent (T2).
- A2A “What A2A is not”: MCP does not specify agent-to-agent payments, mandates, or disputes.
- `oa-w7167155035` “Governance Gaps in Agent Interoperability Protocols: What MCP, A2A, and ACP Cannot Express”.
- No payment, settlement, or L8 artifact in the MCP intro.

## What is not in the packet

No full MCP spec security section extracted here. Measurement paper not re-read beyond the corpus synopsis.
