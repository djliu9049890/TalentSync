from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Dict, Generator, Optional

from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import JobRun


@contextmanager
def job_run(
  job_name: str,
  *,
  db: Optional[Session] = None,
  details: Optional[Dict[str, Any]] = None,
) -> Generator[JobRun, None, None]:
  """
  Context manager that creates a JobRun row and updates it on completion.

  Usage:

    with job_run("posts_ttl_cleanup") as run:
        deleted = delete_expired_posts(db)
        run.details = {"deleted_posts": deleted}
  """
  own_session = db is None
  session = db or SessionLocal()

  run = JobRun(
    job_name=job_name,
    started_at=datetime.now(timezone.utc),
    success=False,
    details=details or {},
  )
  session.add(run)
  session.commit()

  try:
    yield run
    run.success = True
    run.finished_at = datetime.now(timezone.utc)
    session.commit()
  except Exception as exc:  # noqa: BLE001
    run.success = False
    run.finished_at = datetime.now(timezone.utc)
    run.error_message = str(exc)
    session.commit()
    if own_session:
      session.close()
    raise
  finally:
    if own_session:
      session.close()

