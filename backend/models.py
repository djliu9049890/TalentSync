from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
  Column,
  Integer,
  Text,
  DateTime,
  ForeignKey,
  UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped

from .db import Base


class Recruiter(Base):
  __tablename__ = "recruiters"

  id: Mapped[int] = Column(Integer, primary_key=True)
  name: Mapped[str | None] = Column(Text, nullable=True)
  linkedin_profile_url: Mapped[str] = Column(Text, nullable=False, unique=True)
  crawl_slot_hour: Mapped[int] = Column(Integer, nullable=False)  # 0–23
  last_crawled_at: Mapped[datetime | None] = Column(DateTime(timezone=True), nullable=True)

  posts: Mapped[list["Post"]] = relationship(
    "Post",
    back_populates="recruiter",
    cascade="all, delete-orphan",
  )


class Post(Base):
  __tablename__ = "posts"

  id: Mapped[int] = Column(Integer, primary_key=True)
  recruiter_id: Mapped[int] = Column(
    Integer,
    ForeignKey("recruiters.id", ondelete="CASCADE"),
    nullable=False,
  )

  linkedin_post_id: Mapped[str | None] = Column(Text, nullable=True)
  linkedin_post_url: Mapped[str | None] = Column(Text, nullable=True)

  content_text: Mapped[str] = Column(Text, nullable=False)
  posted_at: Mapped[datetime] = Column(
    DateTime(timezone=True),
    nullable=False,
    default=datetime.utcnow,
  )
  raw_html: Mapped[str | None] = Column(Text, nullable=True)
  text_hash: Mapped[str] = Column(Text, nullable=False)

  recruiter: Mapped[Recruiter] = relationship(
    "Recruiter",
    back_populates="posts",
  )

  __table_args__ = (
    UniqueConstraint(
      "linkedin_post_id",
      name="uniq_posts_linkedin_post_id",
    ),
    UniqueConstraint(
      "linkedin_post_url",
      name="uniq_posts_linkedin_post_url",
    )
  )

