"""Execution boundary. No provider or shell types belong here."""

from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

from crossinghouse.contracts.authority import OperationKind
from crossinghouse.contracts.evidence import Evidence
from crossinghouse.contracts.task import TaskContract


class RequestedOperation(BaseModel):
    model_config = ConfigDict(frozen=True)

    kind: OperationKind
    path: str = Field(min_length=1)
    payload: str = ""


class ExecutionRequest(BaseModel):
    """A contract-bound execution attempt."""

    model_config = ConfigDict(frozen=True)

    task: TaskContract
    attempt: int = Field(ge=1)
    operations: tuple[RequestedOperation, ...] = Field(min_length=1)

    @property
    def task_id(self) -> str:
        return self.task.task_id


class ExecutionResult(BaseModel):
    """Execution evidence, deliberately separate from verifier output."""

    model_config = ConfigDict(frozen=True)

    completed: bool
    files_changed: tuple[str, ...] = ()
    claimed_operations: tuple[RequestedOperation, ...] = ()
    evidence: tuple[Evidence, ...] = ()
    error: str | None = None
    uncertainty: str | None = None
    attempt: int = Field(ge=1)


class Executor(Protocol):
    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        """Perform one bounded attempt and return execution-derived evidence."""
