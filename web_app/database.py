"""Database SetUp."""
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from web_app.config import settings

# 1) Whay kind of DB are we communicating with?
# 2) What DBAPI are we using?  Check scheme in config postgresql+psycopg
# 3) How do we locate the DB?
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=True,  # echo=True prints all the SQL statements it executes.
)


SessionLocal = sessionmaker(
    autocommit=False,  # You have to explicitly call .commit() or .rollback().
    autoflush=False,  # Avoid automatic flushes,
    bind=engine,  # Use this SQLAlchemy engine.
    future=True,  # Enable SQLAlchemy 2.0-style behavior.
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session for FastAPI services.

    WARNING: This function should _only_ be called when used with
    using the `Depends` function from FastAPI. This function will leak
    sessions if used outside of the context of a request.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]
