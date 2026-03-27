from __future__ import annotations

import argparse
import json
from datetime import datetime

from backend.crawler_main import crawl_due_recruiters
from backend.db import SessionLocal
from backend.job_logging import job_run


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    description=(
      "Run the crawler immediately without waiting for cron. "
      "Defaults to the current host-machine hour."
    )
  )
  parser.add_argument(
    "--slot",
    type=int,
    choices=range(24),
    metavar="0-23",
    help="Run recruiters assigned to a specific crawl_slot_hour.",
  )
  parser.add_argument(
    "--all-slots",
    action="store_true",
    help="Run the crawler once for each slot from 0 through 23.",
  )
  return parser.parse_args()


def build_now_for_slot(slot_hour: int) -> datetime:
  current_time = datetime.now().astimezone()
  return current_time.replace(hour=slot_hour, minute=0, second=0, microsecond=0)


def run_slot(slot_hour: int) -> dict[str, object]:
  with SessionLocal() as db:
    run_time = build_now_for_slot(slot_hour)
    with job_run("debug_hourly_recruiter_crawl", db=db, details={"slot_hour": slot_hour}) as run:
      summary = crawl_due_recruiters(db, now=run_time)
      summary["debug_requested_slot"] = slot_hour
      run.details = summary
      print(json.dumps(summary, default=str))
      return summary


def run_all_slots() -> list[dict[str, object]]:
  summaries: list[dict[str, object]] = []
  for slot_hour in range(24):
    summaries.append(run_slot(slot_hour))
  return summaries


def main() -> None:
  args = parse_args()

  if args.all_slots:
    summaries = run_all_slots()
    combined = {
      "slots_run": len(summaries),
      "recruiters_selected": sum(summary["recruiters_selected"] for summary in summaries),
      "new_posts_created": sum(summary["new_posts_created"] for summary in summaries),
      "slots": summaries,
    }
    print(json.dumps(combined, default=str))
    return

  slot_hour = args.slot
  if slot_hour is None:
    slot_hour = datetime.now().astimezone().hour

  run_slot(slot_hour)


if __name__ == "__main__":
  main()
