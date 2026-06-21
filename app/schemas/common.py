"""Shared response models used across multiple resources."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    message: str | None = None


class MessageResponse(BaseModel):
    message: str
