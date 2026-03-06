from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from backend/ directory when running from project root or backend/
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)


def get_database_url() -> str:
  """
  Returns the SQLAlchemy database URL.

  Defaults to a local Postgres instance suitable for development:
  postgresql+psycopg2://talentsync:talentsync@localhost:5432/talentsync
  """
  return os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://talentsync:talentsync@localhost:5432/talentsync",
  )

