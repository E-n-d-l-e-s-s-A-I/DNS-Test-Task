from typing import Any
from fastapi import HTTPException


NotFoundException = HTTPException(status_code=404, detail="object not found")

DBIntegrityException = HTTPException(
    status_code=409,
    detail="unique field duplicated or invalid foreign key",
)


def get_http_exceptions_description(
    *http_exceptions: HTTPException,
) -> dict[int, dict[str, Any]]:
    return {
        http_exception.status_code: {
            "description": f"{http_exception.detail}",
            "content": {
                "application/json": {
                    "example": {"detail": f"{http_exception.detail}"}
                }
            },
        }
        for http_exception in http_exceptions
    }
