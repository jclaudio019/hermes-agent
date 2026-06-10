# Lumina Orchestrator Core API Design

Based on the architectural exploration of the Hermes Agent, this document outlines the core architecture for Lumina OS. The guiding principle is that **Lumina owns top-level control**. Hermes may serve as an optional subagent or runtime reference, but Lumina orchestrates the overall execution flow, memory, provider routing, and approval gates.

## Architectural Layers

### 1. Task Intake Layer
*   **Responsibility:** The entry point for all requests, regardless of source.
*   **Functionality:** Normalizes incoming messages from Telegram, the CLI, webhook events, or external systems into a standardized `TaskRequest` object.
*   **Why it's needed:** Disconnects the source of a trigger from the execution pipeline. Ensures that an Obsidian file change, a cron trigger, or a Telegram message all enter the system in the same format.

### 2. Router
*   **Responsibility:** The control brain. It analyzes a `TaskRequest` and determines the best execution path.
*   **Functionality:** Assigns the appropriate provider, runtime, and memory context for a task. For instance, a simple conversational query might route directly to an OpenAI-compatible runtime, while a complex refactoring task might route to a specialized Codex/Jules handoff workflow.
*   **Why it's needed:** Fulfills Lumina's goal of "multi-model routing" and "multi-agent runtime routing."

### 3. Provider Registry
*   **Responsibility:** Manages connections to LLM inference providers.
*   **Functionality:** Maintains configurations for OpenAI, Anthropic, Gemini, local models, etc. It normalizes inputs (prompts) and outputs (completions, tool calls) across different APIs.
*   **Inspiration:** Heavily inspired by Hermes' `ProviderProfile` abstraction, which effectively isolates API quirks from the orchestrator logic.

### 4. Runtime Registry
*   **Responsibility:** Manages the execution environments (agents/subsystems) available to the Router.
*   **Functionality:** Registers and dispatches to specific agent runtimes. This could include a local Python environment, a containerized sandbox, a Jules integration, or even an instance of Hermes via its API server.
*   **Why it's needed:** Allows Lumina to swap out the underlying agent implementation per task without modifying the top-level orchestration layer.

### 5. Tool Registry
*   **Responsibility:** Defines and enforces the capabilities an agent can use.
*   **Functionality:** Maps tool names to their implementations (e.g., `web_search`, `read_obsidian_note`). Crucially, the Router passes *only* the permitted subset of tools to the Runtime for a given task.
*   **Why it's needed:** Granular security. A web browsing task should not be given file deletion tools.

### 6. Memory/Context Layer
*   **Responsibility:** Long-term and short-term cognitive state.
*   **Functionality:** Interfaces with Obsidian or other project memory systems. The Router queries this layer to retrieve relevant context *before* invoking a Runtime, and the Runtime can write back to it. This acts as a unified knowledge graph.
*   **Contrast with Hermes:** Hermes uses a tightly-coupled SQLite WAL database for memory. Lumina abstracts memory so that project state (e.g., Markdown files in an Obsidian vault) acts as the primary source of truth.

### 7. Approval Layer
*   **Responsibility:** Human-in-the-loop security.
*   **Functionality:** Intercepts sensitive tool calls or state modifications (e.g., running `rm -rf`, sending an email) and pauses execution until a human explicitly approves the action via the Intake Layer (e.g., clicking "Approve" in Telegram).
*   **Why it's needed:** Critical for safe autonomous operation, avoiding silent destructive actions.

### 8. Audit/Task State Layer
*   **Responsibility:** Observability and debugging.
*   **Functionality:** Records a structured, append-only log of the task lifecycle: Intake -> Routing -> Memory Retrieval -> Runtime Execution (including tool calls and tokens) -> Result.
*   **Why it's needed:** Supports "project status summaries" and "audit logs," allowing users to see exactly *why* Lumina made a decision or failed a task.

### 9. Artifact/Result Collector
*   **Responsibility:** Formatting and returning the final output.
*   **Functionality:** Takes the raw output from the Runtime and formats it for the Intake Layer. This could mean generating a Markdown summary, updating a specific file, or sending a structured JSON payload back to a webhook.
*   **Why it's needed:** Ensures that regardless of how a task is executed, the user or calling system receives a consistent, usable result.