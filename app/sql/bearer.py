from uuid import uuid4, UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime

BearerBase = declarative_base()

class Bearer(BearerBase):
    __tablename__ = "bearers"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    token = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    last_interaction = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Bearer(id={self.id}, token={self.token}, username={self.username}, last_interaction={self.last_interaction})>"


