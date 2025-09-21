from starlette.middleware.base import BaseHTTPMiddleware

from app.settings.config import get_config

class BearerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.config = get_config()

    async def dispatch(self, request, call_next):
        if request.headers.get('Authorization') is None:
            return None
        else:
            return await call_next(request)