# dedupe.py
import hashlib
from sqlalchemy.orm import Session
from .models import Post

def compute_text_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

def post_exists(
    db: Session,
    *,
    recruiter_id: int,
    linkedin_post_id: str | None,
    linkedin_post_url: str | None,
    text_hash: str,
) -> bool:
    if linkedin_post_id:
        q = db.query(Post).filter(
            Post.recruiter_id == recruiter_id,
            Post.linkedin_post_id == linkedin_post_id,
        )
        if db.query(q.exists()).scalar():
            return True

    if linkedin_post_url:
        q = db.query(Post).filter(
            Post.recruiter_id == recruiter_id,
            Post.linkedin_post_url == linkedin_post_url,
        )
        if db.query(q.exists()).scalar():
            return True

    q = db.query(Post).filter(
        Post.recruiter_id == recruiter_id,
        Post.text_hash == text_hash,
    )
    if db.query(q.exists()).scalar():
        return True

    return False
