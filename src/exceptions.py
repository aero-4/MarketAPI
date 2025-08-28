from enum import Enum, StrEnum
from typing import Optional, Dict, Any

from fastapi import HTTPException
from dataclasses import dataclass

from starlette import status


class ErrorCode(StrEnum):
    NOT_FOUND = "NOT_FOUND"
    NOT_PERMISSIONS = "NOT_PERMISSIONS"
    ALREADY_EXIST = "ALREADY_EXIST"
    UNAVAILABLE_STATUS = "UNAVAILABLE_STATUS"


@dataclass
class AppException(Exception):
    code: ErrorCode
    message: str
    status_code: int = 400
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }


class NotFound(AppException):
    def __init__(self, *, message: str = "Not found", details: Optional[Dict] = None):
        super().__init__(code=ErrorCode.NOT_FOUND,
                         message=message,
                         details=details,
                         status_code=status.HTTP_404_NOT_FOUND)


class NotPermissions(AppException):
    def __init__(self, *, message: str = "No rights for this action", details: Optional[Dict] = None):
        super().__init__(code=ErrorCode.NOT_PERMISSIONS,
                         message=message,
                         details=details,
                         status_code=status.HTTP_403_FORBIDDEN)


class AlreadyExist(AppException):
    def __init__(self, *, message: str = "Already exists", details: Optional[Dict] = None):
        super().__init__(code=ErrorCode.NOT_PERMISSIONS,
                         message=message,
                         details=details,
                         status_code=status.HTTP_400_BAD_REQUEST)


class UnavailableStatus(AppException):
    def __init__(self, *, message: str = "Unavailable status", details: Optional[Dict] = None):
        super().__init__(code=ErrorCode.UNAVAILABLE_STATUS,
                         message=message,
                         details=details,
                         status_code=status.HTTP_403_FORBIDDEN)
