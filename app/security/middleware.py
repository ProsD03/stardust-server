from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response

from app.schema.error import ErrorResponse
from app.settings.config import get_config

class BearerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.config = get_config()

    async def dispatch(self, request, call_next):
        if request.headers.get('Authorization') is None:
            return Response(status_code=401, content=ErrorResponse(error_code="AuthenticationRequired"))
        else:
            return await call_next(request)