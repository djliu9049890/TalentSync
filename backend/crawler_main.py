# crawler.py
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Recruiter, Post
from .dedupe import compute_text_hash, post_exists
from .classifier import classify_post

class SourcePost:
    def __init__(
        self,
        *,
        linkedin_post_id: str | None,
        url: str | None,
        text: str,
        html: str | None,
        posted_at: datetime | None,
    ):
        self.linkedin_post_id = linkedin_post_id
        self.url = url
        self.text = text
        self.html = html
        self.posted_at = posted_at or datetime.utcnow()


def fetch_latest_posts_for_recruiter(recruiter: Recruiter) -> list[SourcePost]:
    """
    Placeholder: implement using your legal/approved data source.
    Must NOT violate LinkedIn's ToS or bypass access controls.
    """
    raise NotImplementedError


def crawl_recruiter(db: Session, recruiter: Recruiter) -> int:
    posts = fetch_latest_posts_for_recruiter(recruiter)
    new_job_posts = 0

    for p in posts:
        text_hash = compute_text_hash(p.text)

        if post_exists(
            db,
            recruiter_id=recruiter.id,
            linkedin_post_id=p.linkedin_post_id,
            linkedin_post_url=p.url
        ):
            continue

        classification = classify_post(p.text)

        if not classification["is_job_post"]:
            continue

        db_post = Post(
            recruiter_id=recruiter.id,
            linkedin_post_id=p.linkedin_post_id,
            linkedin_post_url=p.url,
            content_text=p.text,
            posted_at=p.posted_at,
            raw_html=p.html,
            text_hash=text_hash,
        )
        db.add(db_post)
        new_job_posts += 1

    recruiter.last_crawled_at = datetime.utcnow()
    db.commit()
    return new_job_posts