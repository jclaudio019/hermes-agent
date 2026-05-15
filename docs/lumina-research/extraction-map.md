# Extraction Map

This document outlines the highest-value concepts, files, and patterns in the Hermes Agent repository that Lumina OS should study, extract, or adapt.

## 1. Memory Abstraction
**Files:**
- `agent/memory_provider.py`
- `agent/memory_manager.py`

**Why Study:**
Provides a clean Abstract Base Class (`MemoryProvider`) for hot-swapping memory backends. The `MemoryManager` orchestrates the built-in file store alongside ONE external provider (to prevent schema bloat). The hooks for `on_turn_start`, `on_session_end`, and `on_pre_compress` are excellent design patterns for Lumina's own continuity layer.

## 2. Background Reflection & Curator (Learning Loop)
**Files:**
- `agent/curator.py`
- `tools/skill_manager_tool.py`

**Why Study:**
This is Hermes's defining feature. `tools/skill_manager_tool.py` allows the agent to mutate its own procedural memory (skills). `agent/curator.py` spawns a background, non-blocking LLM task to review agent-generated skills, archive obsolete ones, and merge overlapping ones based on usage heuristics. This "closed learning loop" prevents memory bloat and keeps the agent focused. Lumina should deeply study this background-maintenance pattern.

## 3. Subagent Coordination (Orchestration Logic)
**Files:**
- `tools/delegate_tool.py`

**Why Study:**
Hermes implements subagent generation not as a complex DAG graph, but simply as an LLM tool call. A parent agent uses `delegate_task` to spawn isolated `AIAgent` instances. The parent blocks, while the child receives a restricted toolset (no recursive delegation, no rewriting shared memory) and isolated prompt contexts. This is a robust pattern for parallel task execution.

## 4. Reusable Abstractions & Low-Dependency Components
**Files:**
- `tools/registry.py`: An AST-based, lightweight plugin discovery system for tools. Very low dependency and highly reusable.
- `skills/`: The folder structure itself. Rather than representing skills as Python code, Hermes represents them as markdown files (`SKILL.md`) alongside reference templates. This makes them highly interpretable and mutable by LLMs.
