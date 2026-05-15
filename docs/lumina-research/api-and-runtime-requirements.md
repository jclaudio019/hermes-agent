# API & Runtime Requirements

## Runtime Environments
- **Supported Platforms**: Local (macOS, Linux), WSL2 (Windows Subsystem for Linux), Docker, and various serverless setups (Modal, Daytona). Native Windows is explicitly stated to be in "Early Beta".
- **Language**: Python 3.11+. Node.js is required for certain build steps or bundled skills.
- **Dependencies**: `ffmpeg`, `ripgrep`, and a bundled `git`.

## Core Dependencies
- **Packaging**: Managed via `uv` or standard `pip`.
- **Primary Loop SDKs**: Relies heavily on standard LLM providers.

## Required APIs
- **Model Endpoint**: Requires access to an LLM endpoint. Supports OpenAI-compatible APIs natively.
  - Native integrations include: OpenAI, Anthropic, Bedrock, Gemini, Copilot.
- **SQLite**: Built-in state storage (`hermes_state.py`) relies heavily on SQLite with FTS5 enabled, and `WAL` journal mode (which has constraints on network filesystems like NFS or SMB).

## Optional APIs & Cloud Dependencies
- **Memory Backends**:
  - Honcho (Dialectic user modeling)
  - Mem0
  - Supermemory
- **Platform Webhooks/Long Polling**:
  - Telegram Bot API
  - Discord Bot API
  - Slack Bot API
- **Browser Automation**: CDP-based browser interactions (requires system chromium/browser availability).

## Local-Only Capability Support
- Hermes functions incredibly well in local, air-gapped scenarios provided a local LLM (like Ollama or vLLM) is configured.
- Memory operations (Builtin `MEMORY.md` and `USER.md`) fall back cleanly to the local file system without needing external APIs.

## Authentication Requirements
- **LLM Credentials**: Handled via `.env` or system keychain, managed by `agent/credential_pool.py`.
- **MCP & Tooling Auth**: Supports OAuth for MCP integrations (e.g., Microsoft Graph Auth).
