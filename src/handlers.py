import logging

from starlette.requests import Request
from starlette.responses import JSONResponse

from src.exceptions import AppException

logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exp: AppException):
    logger.warning("AppException: %s %s %s", exp.code, exp.message, exp.details)
    content = exp.to_dict()
    return JSONResponse(status_code=exp.status_code, content=content)
