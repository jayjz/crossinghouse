"""Authority boundaries for an individual task."""

from enum import StrEnum
from pathlib import PurePosixPath

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OperationKind(StrEnum):
    """Operations that a bounded executor may be asked to simulate."""

    MODIFY_FILE = "modify_file"
    CREATE_FILE = "create_file"


def _validate_relative_path(path: str) -> str:
    parsed = PurePosixPath(path)
    if not path or parsed.is_absolute() or ".." in parsed.parts or path == ".":
        raise ValueError("path must be a non-empty relative path without '..'")
    return parsed.as_posix()


class Authority(BaseModel):
    """Immutable scope and operation permissions fixed by a task contract."""

    model_config = ConfigDict(frozen=True)

    allowed_paths: tuple[str, ...] = Field(min_length=1)
    prohibited_operations: tuple[OperationKind, ...] = ()

    @field_validator("allowed_paths")
    @classmethod
    def validate_paths(cls, paths: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(_validate_relative_path(path) for path in paths)
        if len(set(normalized)) != len(normalized):
            raise ValueError("allowed paths must be unique")
        return normalized

    def permits_path(self, path: str) -> bool:
        """Return whether *path* is equal to or below an allowed path."""
        normalized = _validate_relative_path(path)
        return any(
            normalized == allowed or normalized.startswith(f"{allowed}/")
            for allowed in self.allowed_paths
        )

    def permits_operation(self, operation: OperationKind) -> bool:
        return operation not in self.prohibited_operations
