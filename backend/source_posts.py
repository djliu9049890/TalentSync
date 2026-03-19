from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class SourcePost:
  linkedin_post_id: str | None
  url: str | None
  text: str
  html: str | None
  posted_at: datetime = field(default_factory=lambda: datetime.now().astimezone())
