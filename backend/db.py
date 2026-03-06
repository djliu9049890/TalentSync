from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase

from .config import get_database_url


class Base(DeclarativeBase):
  """Base class for all ORM models."""


engine = create_engine(
  get_database_url(),
  pool_pre_ping=True,
)

SessionLocal = scoped_session(
  sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
  )
)


def get_db():
  """
  FastAPI-style dependency helper: yields a session and
  ensures it is closed. Safe to ignore if you don't use FastAPI.
  """
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

