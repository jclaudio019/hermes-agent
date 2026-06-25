# Architecture Overview: Hermes Agent

## High-Level Architecture
Hermes Agent is built to be a self-improving, autonomous AI agent that is platform-independent. The core execution engine can attach to multiple frontends or communication platforms via a single gateway process.

### Key Components

1. **Agent Engine (`run_agent.py`)**
   - The primary autonomous loop executing the conversation and tool calls.
   - Wraps model API providers and handles message history, schema definitions, and retry logic.

2. **Gateway (`gateway/run.py`)**
   - The entry point for multi-platform integration.
   - Standardizes inputs across environments like Local TUI, Telegram, Discord, Slack, etc.
   - Manages routing and asynchronous message streaming to the Agent Engine.

3. **Memory Manager & Providers (`agent/memory_manager.py`, `agent/memory_provider.py`)**
   - Orchestrates one external memory provider along with the built-in system.
   - Handles the injection of persistent context (e.g. `USER.md` and `MEMORY.md`) via system prompt updates.
   - Provides a plugin architecture for different providers (e.g. Mem0, Honcho, Holographic, Supermemory) located in `plugins/memory/`.

4. **Tool Registry & Execution (`tools/registry.py`)**
   - A central registry where tools self-register.
   - Tool execution is abstracted so that tools are just python functions mapped to API schemas, cleanly decoupled from the model loop.

5. **Subagent Delegation (`tools/delegate_tool.py`)**
   - Supports parallel and single-task subagent spawning.
   - Child agents operate in isolated contexts with restricted toolsets, preventing recursive delegation, and their intermediate steps are hidden from the parent.

6. **Skill Manager & Curator (`tools/skill_manager_tool.py`, `agent/curator.py`)**
   - **Skill Manager**: Allows the agent to procedurally store workflows as new skills in the `skills/` directory structure.
   - **Curator**: An independent background orchestrator running on an auxiliary model. It reviews, archives, or refines agent-generated skills based on usage metrics to prevent library bloat.

7. **State Management (`hermes_state.py`)**
   - A SQLite-backed store with FTS5 search.
   - Uses WAL mode to handle concurrent readers (e.g. gateway platforms) and a single writer, with compression for older interactions.

## Execution Model
- **Event-Driven & Polling**: The gateway waits for external signals and triggers `run_conversation()`.
- **Tool-Call Loop**: The core loop iterates on `[System, User, Assistant, Tool Result]` continuously until the model stops issuing tool calls.
- **Daemon/Fork Patterns**: Background components like the Curator run via forked agent instances out of the critical path to maintain latency for the primary agent loop.

## Memory Model
- **Declarative Memory**: Bounded file-backed context containing user preferences and system rules, cached via prefix-caching mechanisms.
- **Procedural Memory (Skills)**: Actionable knowledge stored in `skills/`, containing `SKILL.md` files along with related templates and scripts.
- **Cross-session Memory**: External providers manage vectorized or dialectic knowledge graphs across sessions. Only one external provider operates at a time to prevent tool schema conflict.

## Planning & Orchestration
- Unlike strict multi-agent systems, Hermes relies on a single powerful "Main Agent" that can orchestrate "Child Agents" via the `delegate_task` tool.
- The planning structure relies more on prompt design, reflection tools, and generated procedurals (skills) rather than a rigid external DAG or workflow engine.
