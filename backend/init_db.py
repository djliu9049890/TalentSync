from __future__ import annotations

"""
Simple script to create the database schema in the configured database.

Usage (from project root):

  cd backend
  python init_db.py

Make sure the DATABASE_URL environment variable points at a running Postgres
instance, or that the default URL in config.py matches your local setup.
"""

from .db import engine
from .models import Base  # noqa: F401  - ensures models are registered


def main() -> None:
  Base.metadata.create_all(bind=engine)
  print("Database tables created (or already exist).")


if __name__ == "__main__":
  main()

