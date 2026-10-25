# A2A (Agent2Agent Protocol) — evidence packet

Home layer: L2 / L3. Origin: web2. No `spec-a2a` record in the 304-record corpus; official spec fetched live.

## Canonical locators

- https://a2a-protocol.org/latest/ and https://a2a-protocol.org/latest/topics/key-concepts/
- Spec: https://a2a-protocol.org/latest/specification/
- Paper bib: https://google.github.io/A2A (historical)
- `arxiv-2505.12490v3` privacy/security gaps in Google A2A (overprivilege, long-lived tokens, weak consent)
- `arxiv-2507.19550v1` A2A + ledger identity + x402
- `sur-ehtesham2025-agent-interop`
- UCP A2A transport uses Agent Card URL
- Linux Foundation project; TSC includes AWS, Cisco, Google, IBM, Microsoft, Salesforce, SAP, ServiceNow

## Documented artifacts

- Agent Card: JSON identity, capabilities, endpoint, skills, auth requirements.
- Task: unique ID and lifecycle; Message / Part / Artifact.
- Interaction: request/response polling, SSE streaming, push webhooks.
- Auth declared on the Agent Card; credentials in HTTP headers, not in A2A payloads.
- Opaque agents: no shared internal memory or tools.
- Explicitly complementary to MCP; not a payment or UI protocol.
- Official SDKs: Python, JS, Java, C#, Go, Rust.
- AP2 is described as an extension of A2A for payments.

## Failures named in sources

- `arxiv-2505.12490v3`: overprivilege, long-lived tokens, missing user consent in payment/identity workflows.
- Ledger L2/L3: capability claims and task completion do not prove competence or intent fidelity.
- A2A does not move money, bind AP2 mandates, or provide L8 remedy.
- Task traces support auditability of messages, not recoverability.

## What is not in the packet

Corpus lacks a tagged official A2A spec record. Scoring must rely on the live spec URLs above.
