from __future__ import annotations

from datetime import datetime
from typing import Callable
import json
from pathlib import Path

from sqlalchemy.orm import Session

from . import config as _config  # noqa: F401  - importing loads backend/.env
from .classifier import classify_post
from .db import SessionLocal
from .dedupe import compute_text_hash, post_exists
from .job_logging import job_run
from .linkedin_fetcher import fetch_profile_html
from .models import Post, Recruiter
from .parser import extract_posts_from_profile_html
from .source_posts import SourcePost


HtmlFetcher = Callable[[Recruiter], str]
Parser = Callable[[str], list[SourcePost]]
DEBUG_RENDERED_HTML_PATH = (
  Path(__file__).resolve().parent / "debugging" / "linkedin_gkangj_rendered.html"
)


def fetch_profile_html_for_recruiter(recruiter: Recruiter) -> str:
  """
  Fetch raw recruiter profile HTML with a browser-backed session.

  The parser layer is responsible for isolating the post carousel and
  normalizing it into individual SourcePost entries.
  """
  return fetch_profile_html(recruiter.linkedin_profile_url)


def save_debug_profile_html(profile_html: str) -> None:
  """
  Save the most recently fetched rendered LinkedIn profile HTML for inspection.

  This intentionally writes to the existing debug filename so the current local
  inspection workflow continues to work without new file paths.
  """
  DEBUG_RENDERED_HTML_PATH.write_text(profile_html, encoding="utf-8")


def get_recruiters_for_current_slot(db: Session, *, now: datetime | None = None) -> list[Recruiter]:
  """
  Select recruiters assigned to the current local hour.

  Cron runs this module on the host machine each hour, so using the host's local
  hour keeps the scheduler aligned with the machine where cron is configured.
  """
  current_time = now or datetime.now().astimezone()
  slot_hour = current_time.hour
  return (
    db.query(Recruiter)
    .filter(Recruiter.crawl_slot_hour == slot_hour)
    .order_by(Recruiter.id.asc())
    .all()
  )


def crawl_recruiter(
  db: Session,
  recruiter: Recruiter,
  *,
  fetch_html: HtmlFetcher = fetch_profile_html_for_recruiter,
  parse_posts: Parser = extract_posts_from_profile_html,
) -> int:
  print(f"Fetching {recruiter.name} profile..............")
  profile_html = fetch_html(recruiter)
  # print("Saving profile locally to debug........................")
  # save_debug_profile_html(profile_html)
  print("Parsing profile...........................")
  posts = parse_posts(profile_html)
  # print(posts)
  print("Starting Classification...................")
  new_job_posts = 0

  for post in posts:
    classification = classify_post(post.text)
    print(classification)

    if not classification["is_job_post"]:
      continue

    text_hash = compute_text_hash(post.text)

    linkedin_post_url = post.url

    if post_exists(
      db,
      recruiter_id=recruiter.id,
      linkedin_post_id=post.linkedin_post_id,
      linkedin_post_url=linkedin_post_url,
      text_hash=text_hash,
    ):
      continue

    db_post = Post(
      recruiter_id=recruiter.id,
      linkedin_post_id=post.linkedin_post_id,
      linkedin_post_url=linkedin_post_url,
      content_text=post.text,
      posted_at=post.posted_at,
      raw_html=post.html,
      text_hash=text_hash,
      job_title=classification["title"],
      company=classification["company"],
      location=classification["location"],
      employment_type=classification["employment_type"],
      salary=classification["salary"],
      hiring_contact=classification["hiring_contact"],
      extraction_payload=classification,
    )
    db.add(db_post)
    new_job_posts += 1
    print("post " + post.url + " added")

  recruiter.last_crawled_at = datetime.now().astimezone()
  db.commit()
  return new_job_posts


def crawl_due_recruiters(
  db: Session,
  *,
  now: datetime | None = None,
  fetch_html: HtmlFetcher = fetch_profile_html_for_recruiter,
  parse_posts: Parser = extract_posts_from_profile_html,
) -> dict[str, object]:
  recruiters = get_recruiters_for_current_slot(db, now=now)
  recruiter_results: list[dict[str, object]] = []
  total_new_posts = 0

  for recruiter in recruiters:
    recruiter_summary = {
      "recruiter_id": recruiter.id,
      "recruiter_name": recruiter.name,
      "linkedin_profile_url": recruiter.linkedin_profile_url,
      "crawl_slot_hour": recruiter.crawl_slot_hour,
    }

    try:
      created = crawl_recruiter(
        db,
        recruiter,
        fetch_html=fetch_html,
        parse_posts=parse_posts,
      )
      recruiter_summary["new_posts"] = created
      recruiter_summary["status"] = "success"
      total_new_posts += created
    except NotImplementedError as exc:
      db.rollback()
      recruiter_summary["new_posts"] = 0
      recruiter_summary["status"] = "skipped"
      recruiter_summary["error"] = str(exc)
    except Exception as exc:  # noqa: BLE001
      db.rollback()
      recruiter_summary["new_posts"] = 0
      recruiter_summary["status"] = "error"
      recruiter_summary["error"] = str(exc)

    recruiter_results.append(recruiter_summary)

  current_time = now or datetime.now().astimezone()
  return {
    "slot_hour": current_time.hour,
    "recruiters_selected": len(recruiters),
    "new_posts_created": total_new_posts,
    "recruiters": recruiter_results,
  }


def main() -> None:
  with SessionLocal() as db:
    with job_run("hourly_recruiter_crawl", db=db) as run:
      summary = crawl_due_recruiters(db)
      run.details = summary
      print(json.dumps(summary, default=str))


if __name__ == "__main__":
  main()
