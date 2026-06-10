"""
Lumina Orchestrator Core API Skeleton.

This file provides minimal abstract base classes and protocols demonstrating the
architecture defined in lumina_orchestrator_design.md. It establishes that Lumina
retains top-level control over execution.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol


# --- 1. Task Intake Layer ---

@dataclass
class TaskRequest:
    source: str          # e.g., 'telegram', 'cli', 'cron'
    intent: str          # The raw request, e.g., "Summarize the latest logs"
    metadata: Dict[str, Any] # e.g., user_id, timestamps

class IntakeLayer(Protocol):
    def receive(self, raw_input: Any) -> TaskRequest: ...


# --- 6. Memory/Context Layer ---

@dataclass
class ContextPayload:
    system_prompt: str
    relevant_memories: List[str]

class MemoryLayer(ABC):
    @abstractmethod
    def retrieve_context(self, task: TaskRequest) -> ContextPayload: ...

    @abstractmethod
    def store_memory(self, content: str, source: str) -> None: ...


# --- 5. Tool Registry ---

class Tool(Protocol):
    name: str
    description: str

    def execute(self, **kwargs) -> Any: ...

class ToolRegistry(ABC):
    @abstractmethod
    def get_allowed_tools(self, task: TaskRequest) -> List[Tool]: ...


# --- 3. Provider Registry ---

class ProviderProfile(Protocol):
    name: str
    supports_vision: bool

class ProviderRegistry(ABC):
    @abstractmethod
    def resolve_provider(self, constraints: Dict[str, Any]) -> ProviderProfile: ...


# --- 7. Approval Layer ---

class ApprovalLayer(ABC):
    @abstractmethod
    def requires_approval(self, action_type: str, details: Dict[str, Any]) -> bool: ...

    @abstractmethod
    def request_approval(self, task: TaskRequest, action_type: str) -> bool: ...


# --- 4. Runtime Registry ---

@dataclass
class ExecutionResult:
    success: bool
    final_output: str
    artifacts: List[str]

class AgentRuntime(ABC):
    """
    An execution environment (could be Hermes API, local Python, etc.).
    """
    @abstractmethod
    def execute(self, task: TaskRequest, context: ContextPayload, tools: List[Tool], provider: ProviderProfile) -> ExecutionResult: ...

class RuntimeRegistry(ABC):
    @abstractmethod
    def select_runtime(self, task: TaskRequest) -> AgentRuntime: ...


# --- 8. Audit/Task State Layer ---

class AuditLogger(ABC):
    @abstractmethod
    def log_event(self, task_id: str, event_type: str, details: Dict[str, Any]) -> None: ...


# --- 9. Artifact/Result Collector ---

class ResultCollector(ABC):
    @abstractmethod
    def format_and_deliver(self, result: ExecutionResult, original_task: TaskRequest) -> None: ...


# --- 2. Router (The Control Brain) ---

class LuminaRouter(ABC):
    """
    The central orchestrator that glues the layers together.
    """
    def __init__(self,
                 provider_registry: ProviderRegistry,
                 runtime_registry: RuntimeRegistry,
                 tool_registry: ToolRegistry,
                 memory_layer: MemoryLayer,
                 approval_layer: ApprovalLayer,
                 audit_logger: AuditLogger,
                 result_collector: ResultCollector):
        self.providers = provider_registry
        self.runtimes = runtime_registry
        self.tools = tool_registry
        self.memory = memory_layer
        self.approval = approval_layer
        self.audit = audit_logger
        self.results = result_collector

    @abstractmethod
    def route_and_execute(self, task: TaskRequest) -> None:
        """
        Implementation outline:
        1. Log task initiation.
        2. Determine required provider & runtime.
        3. Retrieve context from Memory layer.
        4. Select safe subset of Tools from Tool Registry.
        5. Pass execution to Runtime.
        6. (During execution, runtime callbacks check Approval Layer).
        7. Collect ExecutionResult and pass to Result Collector.
        """
        pass
