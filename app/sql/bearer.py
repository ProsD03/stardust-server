from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Bearer(Base):
    __tablename__ = "bearers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)

    def __repr__(self):
        return f"<Bearer(id={self.id}, token={self.token}, username={self.username})>"


