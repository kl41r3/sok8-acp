# AG-UI (Agent–User Interaction Protocol) — evidence packet

Home layer: L7. Origin: web2. **No `spec-*` record in the 304-record corpus.** Official docs fetched live.

## Canonical locators

- https://docs.ag-ui.com/ (redirect from https://ag-ui.com)
- Paper bib `agui`: https://ag-ui.com
- GitHub https://github.com/ag-ui-protocol/ag-ui
- Positions itself as the agent↔user layer next to MCP (tools) and A2A (agents)
- Distinct from A2UI (generative UI widgets)

## Documented artifacts

- Event-based protocol for streaming agent state, UI intents, and user interactions.
- Building blocks: streaming chat, multimodality, generative UI, shared state, thinking-step visualization, frontend tool calls, interrupts (HITL: pause, approve, edit, retry), agent steering, custom events.
- Many framework integrations (LangGraph, CrewAI, ADK, Microsoft Agent Framework, Mastra, Pydantic AI, etc.) and SDKs (Kotlin, Go, Dart, Java, Rust).
- Clients include CopilotKit; also terminal and chat-platform clients.
- Originated from CopilotKit partnerships; now an open protocol.

## Failures named in sources

- Ledger L7 / T5: interface transparency does not create enforceable remedy. AG-UI documents interrupts and observability, not payment recourse.
- No mandate, settlement, or dispute objects in the overview.
- Corpus hit count for AG-UI was 1 and was a false positive. All scoring evidence is the live docs, not the tagged corpus.
- Docs themselves warn that agents are long-running and nondeterministic; the protocol does not make them auditable for L4/L5/L8 properties.

## What is not in the packet

No event-schema dump. No independent adoption census beyond the integration table on the docs site.
