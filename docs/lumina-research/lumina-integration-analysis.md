# Lumina Integration Analysis

## Overview
Hermes Agent is built as a complete product (Gateway + UI + Execution + Storage) rather than an embedded library. Because Lumina OS V3 acts as a cognitive orchestrator and memory/routing layer, deeply integrating Hermes by calling its internal Python APIs is risky. However, specific functional concepts and components are extremely valuable.

## What Lumina Should Use Directly
- **Nothing as an internal dependency.** Hermes relies on heavy state assumptions (`hermes_state.py`, `~/.hermes/`), and its `run_agent.py` loops tightly couple to this state.
- **Instead:** Lumina should run Hermes as a sidecar/external container if it wishes to utilize its "gateway + multi-platform routing" or simply treat Hermes as another "Agent Provider" behind a standardized API.

## What Should Remain External
- **Gateway & Platform Adapters (`gateway/`)**: Discord, Telegram, and Slack polling logic are comprehensive but complex. If Lumina wants platform connectivity, it should run Hermes as the edge node or maintain a clean separation.
- **Subagent Runtime (`tools/delegate_tool.py`)**: The specifics of how Hermes spawns its subagents are highly customized for its CLI/TUI outputs. Lumina has its own intelligence coordination and shouldn't inherit Hermes's threading models.

## What Should Eventually Be Extracted Internally
- **Memory Provider Interface (`agent/memory_provider.py`)**: The abstraction for hot-swapping memory backends (Honcho, Mem0, Supermemory) is excellent and could inspire Lumina's own memory provider abstraction.
- **Procedural Memory Loop (Skill Curator)**: The `agent/curator.py` and `tools/skill_manager_tool.py` represent a robust learning loop. Lumina should extract the *concept* and *prompt engineering* of background skill refinement (archiving, pinning, updating) and implement it natively within the Lumina OS orchestrator.
- **File Fencing Contexts**: The prompt building mechanisms that fence memory (`<memory-context>`) to avoid prompt injection and optimize prefix caching.

## Tightly Coupled & Risky Subsystems
- **`run_agent.py` / Agent Loop**: Highly coupled to `hermes_state.py`, SQLite schemas, and global configuration logic. Trying to rip out the Hermes Agent runtime loop and embedding it in Lumina's core will cause significant technical debt.
- **State Store (`hermes_state.py`)**: The SQLite FTS5 store is highly specific to the conversational history requirements of Hermes and would conflict with Lumina's centralized memory models.

## Stable & Reusable Abstractions
- **Tool Registry (`tools/registry.py`)**: A very simple and elegant way of decoupled tool registration.
- **Skill Structure (`skills/`)**: The folder layout (`SKILL.md`, `references/`, `scripts/`) is a stable paradigm for representing agent capabilities that Lumina can adopt.
