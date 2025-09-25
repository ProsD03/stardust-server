import argparse
import base64
import secrets
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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


def create_bearer(username: str):
    db = create_engine("sqlite:///data/sqlite.db")
    BearerBase.metadata.create_all(db)
    session = sessionmaker(bind=db)()

    token = f"sds-{secrets.token_urlsafe(120)}"
    bearer = Bearer(
        username=username,
        token=token
    )

    session.add(bearer)
    session.commit()

    print(f"✅ Created bearer for {username}")
    print(f"   ID: {bearer.id}")
    print(f"   Token: {bearer.token}")


def main():
    parser = argparse.ArgumentParser(description="Create a new Bearer")
    parser.add_argument("username", help="The username for the bearer")
    args = parser.parse_args()

    create_bearer(args.username)


if __name__ == "__main__":
    main()