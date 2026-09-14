"""Structured, provider-neutral evidence carried between kernel boundaries."""

from pydantic import BaseModel, ConfigDict, Field


class Evidence(BaseModel):
    """A small immutable evidence item; persistence is deliberately out of scope."""

    model_config = ConfigDict(frozen=True)

    kind: str = Field(min_length=1)
    detail: str = Field(min_length=1)
