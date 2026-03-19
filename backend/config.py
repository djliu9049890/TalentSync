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


def get_env_flag(name: str, default: bool = False) -> bool:
  value = os.getenv(name)
  if value is None:
    return default
  return value.strip().lower() in {"1", "true", "yes", "on"}


def get_linkedin_cookie_li_at() -> str | None:
  return os.getenv("LINKEDIN_COOKIE_LI_AT")


def get_linkedin_headless() -> bool:
  return get_env_flag("LINKEDIN_HEADLESS", default=True)


def get_linkedin_page_load_timeout() -> int:
  return int(os.getenv("LINKEDIN_PAGE_LOAD_TIMEOUT", "45"))


def get_linkedin_wait_timeout() -> int:
  return int(os.getenv("LINKEDIN_WAIT_TIMEOUT", "20"))


def get_linkedin_post_load_scrolls() -> int:
  return int(os.getenv("LINKEDIN_POST_LOAD_SCROLLS", "3"))
