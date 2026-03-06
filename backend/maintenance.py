from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from .db import SessionLocal
from .job_logging import job_run
from .models import Post


RETENTION_DAYS = 90  # ~3 months


def delete_expired_posts(db: Session, *, retention_days: int = RETENTION_DAYS) -> int:
  """
  Delete posts older than `retention_days` based on their `posted_at` timestamp.

  Returns the number of rows deleted.
  """
  cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)

  deleted = (
    db.query(Post)
    .filter(Post.posted_at < cutoff)
    .delete(synchronize_session=False)
  )

  db.commit()
  return deleted


def main() -> None:
  with SessionLocal() as db:
    with job_run("posts_ttl_cleanup", db=db) as run:
      deleted = delete_expired_posts(db)
      run.details = {"deleted_posts": deleted, "retention_days": RETENTION_DAYS}
      print(f"Deleted {deleted} posts older than {RETENTION_DAYS} days.")


if __name__ == "__main__":
  main()

