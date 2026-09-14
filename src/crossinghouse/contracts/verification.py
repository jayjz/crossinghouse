"""Verification results produced independently of execution self-reports."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from crossinghouse.contracts.evidence import Evidence


class VerificationStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    INDETERMINATE = "indeterminate"


class VerificationResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    check_id: str = Field(min_length=1)
    status: VerificationStatus
    evidence: tuple[Evidence, ...] = ()
    reason: str = Field(min_length=1)

    @property
    def passed(self) -> bool:
        return self.status is VerificationStatus.PASS
