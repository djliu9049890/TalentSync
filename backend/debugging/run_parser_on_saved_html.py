from __future__ import annotations

import argparse
import json
from pathlib import Path

from backend.parser import extract_post_carousel_html, extract_posts_from_profile_html


DEFAULT_INPUT_PATH = Path(__file__).resolve().parent / "linkedin_gkangj_rendered.html"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "parser_output"


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    description="Run the LinkedIn carousel parser on a saved HTML file."
  )
  parser.add_argument(
    "input_html",
    nargs="?",
    default=str(DEFAULT_INPUT_PATH),
    help="Path to the saved rendered profile HTML file.",
  )
  parser.add_argument(
    "--output-dir",
    default=str(DEFAULT_OUTPUT_DIR),
    help="Directory for extracted parser artifacts.",
  )
  return parser.parse_args()


def main() -> None:
  args = parse_args()
  input_path = Path(args.input_html).resolve()
  output_dir = Path(args.output_dir).resolve()
  posts_dir = output_dir / "posts"
  output_dir.mkdir(parents=True, exist_ok=True)
  posts_dir.mkdir(parents=True, exist_ok=True)

  profile_html = input_path.read_text(encoding="utf-8", errors="replace")
  carousel_html = extract_post_carousel_html(profile_html)
  posts = extract_posts_from_profile_html(profile_html)

  carousel_output_path = output_dir / "carousel.html"
  carousel_output_path.write_text(carousel_html, encoding="utf-8")

  post_summaries: list[dict[str, object]] = []
  for index, post in enumerate(posts, start=1):
    post_html_path = posts_dir / f"post_{index:02d}.html"
    post_html_path.write_text(post.html or "", encoding="utf-8")
    post_summaries.append(
      {
        "index": index,
        "html_path": str(post_html_path),
        "url": post.url,
        "text_preview": post.text[:200],
      }
    )

  summary = {
    "input_html": str(input_path),
    "carousel_html": str(carousel_output_path),
    "post_count": len(posts),
    "posts": post_summaries,
  }

  summary_output_path = output_dir / "summary.json"
  summary_output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

  print(json.dumps(summary, indent=2))


if __name__ == "__main__":
  main()
