# Lumina OS: Master Architecture Blueprint

This document represents the unified technical blueprint for **Lumina OS**, derived from an exhaustive architectural audit of the donor repositories in this workspace (notably `Hermes-Agent` and its associated memory plugins, specifically `honcho`).

> **Note:** The user prompt implies the existence of `dexter-free`, `OpenJarvis`, and `OpenBrainAI` within the workspace. Extensive searches across the container filesystem confirm these repositories are *not* present in the current workspace mount. Therefore, sections referencing them must be extrapolated conceptually based on standard design patterns for financial workflows and environment tools, combined with the capabilities native to Hermes.

---

## 1. Donor Mapping Matrix

| Lumina OS Component | Donor Source | Key Files & Classes to Extract |
| :--- | :--- | :--- |
| **Lumina Gatekeeper (Upfront Planning)** | `Hermes-Agent` | `agent/conversation_loop.py` (Turn management), `gateway/run.py` (Messaging adapters), `agent/prompt_builder.py` (System context assembly). |
| **Hybrid DAG Execution Engine** | `Hermes-Agent` | `agent/tool_executor.py` (`_execute_tool_calls_concurrent`), `tools/delegate_tool.py` (Subagent spawning). |
| **Dialectic Memory (Reasoning Infrastructure)** | `honcho` plugin | `plugins/memory/honcho/session.py` (Session dialectic wrapper), `plugins/memory/honcho/client.py` (API interface), `plugins/memory/honcho/cli.py` (Dialectic configuration). |
| **Financial Deep Research Skills** | N/A (`dexter-free` missing) | Conceptually maps to tools extending `tools/web_search_provider.py` or new specialized implementations in `tools/`. |
| **Environment & System Tools** | `Hermes-Agent` | `tools/file_operations.py` (File I/O), `tools/terminal_tool.py` (Shell execution), `tools/computer_use/` (Decoupled system tools). |

---

## 2. Unified Data Flow Map

This traces the end-to-end execution of a user command through the Lumina OS architecture.

1.  **Gatekeeper / Task Intake**
    *   User sends a command (e.g., via Telegram Gateway).
    *   Lumina normalizes the intent and parses parameters.
    *   *Halt / Approval Gate:* If the command is high-stakes (e.g., "execute massive trade"), Lumina prompts the user with a proposed plan and requires explicit approval before continuing.

2.  **Honcho Memory Injection (Pre-execution)**
    *   Lumina queries the `Honcho` Dialectic Engine to inject context.
    *   It retrieves user preferences, past financial strategies, and relevant project goals.
    *   The `System Prompt` is built combining task instructions + Honcho context.

3.  **Hybrid DAG Execution & Tool Invocation**
    *   The orchestrator initiates a planning step (Macro-plan).
    *   It executes Task N (e.g., "Retrieve AAPL market data").
    *   *Concrete Evaluation:* Before proceeding to Task N+1, the orchestrator evaluates the output of Task N. If the data is insufficient, it dynamically rewires the DAG to execute a corrective step (e.g., "Search SEC filings instead").

4.  **Specialized Financial Verification**
    *   During execution, specialized financial tools are called (formerly `dexter-free` logic).
    *   These tools don't just return data; they return *structured validation* (e.g., "Is this data sufficient to model the P/E ratio?").

5.  **Post-Turn Dialectic Reflection (Dream Layer)**
    *   After the execution finishes and the user is answered, Lumina triggers a background reflection step.
    *   The `Honcho` engine analyzes the session trajectory.
    *   It synthesizes new observations, updates user preferences, and commits reasoning paths to long-term memory for future tasks.

---

## 3. Proposed Directory Structure

To keep Lumina OS clean, decoupled from heavy UI wrappers, and in top-level control, the extracted components will live in `lumina-core/`:

```text
lumina-core/
├── intake/
│   ├── gatekeeper.py           # Upfront conversational planner & approval gates
│   └── adapters/               # Telegram, CLI, Webhook inputs
├── orchestrator/
│   ├── hybrid_dag.py           # Dynamic Planning/Action/Validation execution loop
│   ├── router.py               # Top-level control, provider selection
│   └── evaluator.py            # Concrete outcome evaluation between DAG steps
├── memory/
│   ├── dialectic_engine.py     # Wraps Honcho for multi-pass reasoning extraction
│   └── project_graph.py        # Obsidian / Local Markdown project memory
├── skills/
│   ├── system/                 # Clean, modular Python primitives (from OpenJarvis/Hermes)
│   │   ├── shell.py
│   │   └── file_io.py
│   └── financial/              # Decomposed quantitative queries (from dexter-free)
│       ├── market_data.py
│       └── verification.py
└── providers/
    └── llm_registry.py         # Standardized interface to OpenAI, Anthropic, etc.
