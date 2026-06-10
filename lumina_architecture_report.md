# Lumina OS: Hermes Agent Foundation Architecture Exploration

This report analyzes the [Nous Research Hermes Agent](https://github.com/nousresearch/hermes-agent) repository to evaluate its suitability as a foundation layer, runtime subsystem, or reference implementation for Lumina OS.

## 1. What does Hermes already provide?

Hermes Agent provides a robust, standalone agent framework with several advanced capabilities:

*   **Multi-Platform Gateway:** A `gateway` system (`gateway/platforms/`) that supports messaging platforms like Telegram, Discord, Slack, WhatsApp, Signal, WeChat/WeCom, DingTalk, and Email.
*   **LLM Provider Abstraction:** A sophisticated provider registry (`providers/`, `agent/transports/`) that normalizes APIs for OpenAI, Anthropic, Bedrock, Gemini, OpenRouter, Azure, and others. It separates auth, capabilities (e.g., vision), endpoints, and prompt formatting.
*   **Persistent State & Memory:** Uses SQLite (`hermes_state.py`) with FTS5 for full-text search, persistent session storage, and long-term memory via the `memory_manager.py` and Honcho integration.
*   **Skill/Tool System:** An extensive tool system (`tools/`, `skills/`) supporting computer use, file operations, web browsing, cron scheduling, code execution, and dynamic skill curation.
*   **Agent Runtime Loop:** A stateful `AIAgent` orchestrator (`agent/`) that manages turn-based conversation loops, context compression, rate limiting, and tool execution.
*   **API Server:** An OpenAI-compatible API server (`gateway/platforms/api_server.py`) allowing external UIs to connect to Hermes.

## 2. What can Lumina reuse?

Several components in Hermes are well-designed and highly modular, making them excellent candidates for extraction or reference:

*   **Provider Abstraction (`providers/` and `agent/transports/`):** The declarative `ProviderProfile` system is excellent for multi-model routing and normalizing different model APIs into a unified format (`NormalizedResponse`, `ToolCall`).
*   **Gateway Adapters (`gateway/platforms/`):** The logic for interfacing with Telegram, Slack, etc., is highly reusable. Lumina can reference these adapters to build its mobile/Telegram control layer.
*   **Tool/Skill Implementations (`tools/`):** Specific tool implementations (e.g., `browser_tool.py`, `file_operations.py`, `computer_use/`) are self-contained and could be reused in Lumina's tool-enabled agent behavior.
*   **Context Compression:** Algorithms for trajectory compression and context summarization (`agent/context_compressor.py`, `agent/conversation_compression.py`).

## 3. What can Lumina wrap safely?

Lumina could safely wrap the Hermes Agent as a **subagent** or an **API service**:

*   **API Server:** Lumina could start Hermes as an API server (`hermes gateway start` with `api_server` enabled) and interact with it via the standard OpenAI Chat Completions API. This allows Lumina to use Hermes as an execution engine.
*   **Isolated Runtimes:** Lumina could spawn Hermes via its CLI (`hermes_cli/`) or as a subprocess for isolated tasks, leveraging its built-in persistence and tools.

## 4. What is too coupled to Hermes?

Certain core components are deeply intertwined and would be difficult to extract or replace within the Hermes architecture:

*   **State Management (`hermes_state.py`):** The SQLite WAL database is heavily coupled to how Hermes manages sessions, active session leases, and kanban tasks. Integrating this directly with Lumina's "Obsidian/project memory" would require significant rewiring.
*   **The `AIAgent` Orchestrator:** The main agent loop in `run_agent.py` and its helpers (`agent/agent_runtime_helpers.py`, `agent/conversation_loop.py`) handle everything from UI display to context management. It is not designed to be easily swapped out for a different cognitive architecture (like Codex/Jules handoff workflows).
*   **CLI vs. Gateway Duality:** Hermes splits its execution model between a rich TUI (`hermes_cli/curses_ui.py`) and a headless Gateway (`gateway/run.py`). This duality introduces complexity (e.g., cross-process session leases) that might conflict with Lumina's orchestrator design.

## 5. What is missing for Lumina?

Hermes Agent lacks several higher-level orchestration features required for Lumina OS:

*   **Multi-Agent Routing:** Hermes focuses on a *single* primary agent per session (though it has subagent delegation). It lacks a true "multi-agent runtime routing" layer that dynamically selects different agents (e.g., Jules vs. Claude) for different tasks.
*   **Deterministic Task Bundles & Workflows:** Hermes is highly conversational and reactive. It lacks a strong framework for deterministic, graph-based workflows or explicit approval gates for multi-step risky actions.
*   **Deep Memory Integration:** While Hermes has memory, Lumina specifically wants "Obsidian/project memory integration" which goes beyond SQLite FTS search and into active knowledge graph management.
*   **Project Status Summaries & Audit Logs:** Hermes has logs and history, but lacks native high-level project status summaries and structured audit logs suitable for a "cognitive status panel."

## 6. Should Lumina wrap, fork, extract, or keep Hermes separate?

**Recommendation: Extract and Keep Separate (Reference Implementation)**

Lumina should **not** build directly on top of or fork Hermes Agent.

*   **Why not fork/build on top?** As noted in the prompt, adding custom providers or tweaking specific behaviors causes friction. Hermes is highly opinionated about its state management, TUI, and agent loop. Forcing Lumina's goals (multi-agent routing, specific UI layers, Obsidian memory) into Hermes would require gutting its core.
*   **Why extract and reference?** Hermes is an incredible reference for *how* to build resilient LLM interactions. Lumina should extract the best parts:
    *   Extract the `ProviderProfile` pattern for multi-model routing.
    *   Extract or reference the Gateway adapters (Telegram, etc.).
    *   Extract specific skills/tools.

Lumina should be built as a separate "cognitive orchestrator" that can *call* Hermes as one of its available agents (via API), but Lumina must own the top-level runtime, routing, and memory.

## 7. What should the next task be after this exploration?

The next task should be to design the **Lumina Orchestrator Core API**.

1.  **Define the Router:** Create a lightweight framework for receiving tasks (via CLI or Telegram) and routing them to a specific handler or agent.
2.  **Extract the Provider Interface:** Port the `ProviderProfile` concept from Hermes into Lumina to establish a clean foundation for multi-model usage.
3.  **Prototype the Memory Abstraction:** Design the interface for the Obsidian/project memory system before building out complex agent loops.