# Adapter Recommendation

Because `run_agent.py` and `gateway/run.py` are heavily intertwined with global configurations and SQLite states (`hermes_state.py`), trying to import Hermes as a native Python library within Lumina OS is risky and will lead to unmanageable state collisions.

## Recommended Design: Docker Service + API Wrapper

Lumina OS should treat Hermes as a black-box execution node for specific platform integrations or isolated tasks.

### Architecture

1. **Dockerized Service**
   - Run Hermes Agent as a standalone Docker container alongside Lumina OS.
   - Map a dedicated volume to `~/.hermes/` for Hermes to handle its state cleanly without interfering with Lumina's databases.

2. **API Wrapper Integration (Recommended over MCP for core control)**
   - Expose Hermes via a simple HTTP or RPC layer (if it doesn't natively expose an API for non-gateway invocations, write a lightweight FastAPI wrapper that triggers `AIAgent.run_conversation()`).
   - *Lumina Orchestrator* sends tasks to the *Hermes Wrapper API*.
   - *Hermes Wrapper* handles the loop, saves the result, and webhooks the summary back to Lumina.

3. **MCP Integration (Alternative)**
   - If Hermes implements MCP (Model Context Protocol) natively or via a tool (e.g. `mcp_tool.py`), Lumina could expose its own services to Hermes via MCP, or vice versa, interact with Hermes's tools. However, for orchestrating the *agent itself*, an API wrapper is more robust.

### Recommended Interface Shape (API Wrapper)

```json
POST /v1/agent/task
{
  "session_id": "lumina_task_xyz",
  "task": "Investigate repo X and generate a bug report",
  "context": "Context passed from Lumina's persistent memory",
  "allowed_tools": ["file_operations", "browser", "execute_code"]
}
```

### Risks and Maintenance Concerns
- **State Drift:** If Lumina relies on Hermes to do work, Hermes's internal `MEMORY.md` and skills will diverge from Lumina's central knowledge graph.
- **Mitigation:** Run Hermes ephemerally for Lumina tasks (wiping `~/.hermes/` on boot), OR periodically sync Hermes's `SKILL.md` library back into Lumina's core knowledge store.
- **Upgrade Paths:** Keeping them as separate containers means updating the Hermes image won't break the Lumina core, provided the wrapper API contract remains intact.
