import re
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response

from app.schema.error import ErrorResponse
from app.settings.config import get_config
from app.sql.bearer import Bearer, BearerBase


class BearerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.config = get_config()
        self.db = create_engine("sqlite:///data/sqlite.db")
        self.token_regex = re.compile(r"sds-.*")

        BearerBase.metadata.create_all(self.db)

    async def dispatch(self, request, call_next):
        if request.headers.get('Authorization') is None:
            return Response(status_code=401,
                            content=ErrorResponse(error_code="AuthenticationRequired").model_dump_json())

        token = request.headers.get('Authorization').split(" ")[1]
        if not self.token_regex.match(token):
            return Response(status_code=401,
                            content=ErrorResponse(error_code="AuthenticationFailed").model_dump_json())

        session = sessionmaker(bind=self.db)()
        bearer = session.query(Bearer).filter_by(token=token).first()
        if not bearer:
            return Response(status_code=401,
                            content=ErrorResponse(error_code="AuthenticationFailed").model_dump_json())

        bearer.last_interaction = datetime.now()
        session.commit()

        request.state.user_id = bearer.id

        return await call_next(request)
