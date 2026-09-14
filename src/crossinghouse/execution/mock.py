"""A deterministic executor for tests; it never writes to the filesystem."""

from crossinghouse.contracts.evidence import Evidence
from crossinghouse.execution.base import ExecutionRequest, ExecutionResult, Executor


class MockExecutor(Executor):
    """Simulate operations only when the immutable task authority permits them."""

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        for operation in request.operations:
            if not request.task.authority.permits_path(operation.path):
                return self._denied(
                    request, f"path outside authority: {operation.path}"
                )
            if not request.task.authority.permits_operation(operation.kind):
                return self._denied(
                    request, f"operation prohibited: {operation.kind.value}"
                )

        changed = tuple(operation.path for operation in request.operations)
        return ExecutionResult(
            completed=True,
            files_changed=changed,
            claimed_operations=request.operations,
            evidence=(
                Evidence(
                    kind="mock_execution", detail="authorized operations simulated"
                ),
            ),
            attempt=request.attempt,
        )

    @staticmethod
    def _denied(request: ExecutionRequest, reason: str) -> ExecutionResult:
        return ExecutionResult(
            completed=False,
            evidence=(Evidence(kind="mock_execution", detail="operation denied"),),
            error=reason,
            attempt=request.attempt,
        )
