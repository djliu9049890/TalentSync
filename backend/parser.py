from __future__ import annotations

import re

from bs4 import BeautifulSoup, Tag

from .source_posts import SourcePost

LINKEDIN_BASE_URL = "https://www.linkedin.com"
LINKEDIN_ACTIVITY_URN_PATTERN = re.compile(r"(urn:li:activity:\d+)")
HYDRATED_POST_LIMIT = 12


def _tag_contains_carousel(tag: Tag) -> bool:
  for value in tag.attrs.values():
    values = value if isinstance(value, list) else [value]
    for item in values:
      if item and "carousel" in str(item).lower():
        return True
  return False


def _find_carousel_candidates(soup: BeautifulSoup) -> list[Tag]:
  return [
    tag
    for tag in soup.find_all("ul")
    if _tag_contains_carousel(tag)
  ]


def _require_carousel_candidates(soup: BeautifulSoup) -> list[Tag]:
  candidates = _find_carousel_candidates(soup)
  if not candidates:
    raise ValueError("Could not find any LinkedIn carousel <ul> elements in profile HTML.")
  return candidates


def extract_post_carousel_html(profile_html: str) -> str:
  """
  Placeholder for isolating the post carousel from the full LinkedIn profile HTML.

  This exists as a separate step so the browser fetcher can stay dumb and
  resilient: it returns the full page HTML, and the parser layer decides how to
  narrow that down before asking an LLM to split it into posts.
  """
  soup = BeautifulSoup(profile_html, "html.parser")
  carousels = _require_carousel_candidates(soup)
  return "\n".join(str(carousel) for carousel in carousels)


def _extract_post_text(post_node: Tag) -> str:
  return post_node.get_text(" ", strip=True)


def _extract_post_url(post_node: Tag) -> str | None:
  for link in post_node.find_all("a", href=True):
    href = str(link["href"]).strip()
    if "/feed/update/" not in href:
      continue
    if href.startswith("http://") or href.startswith("https://"):
      return href
    if href.startswith("/"):
      return f"{LINKEDIN_BASE_URL}{href}"
    return f"{LINKEDIN_BASE_URL}/{href.lstrip('/')}"

  return None


def _extract_post_id(post_url: str | None) -> str | None:
  if not post_url:
    return None

  match = LINKEDIN_ACTIVITY_URN_PATTERN.search(post_url)
  if match:
    return match.group(1)

  return None


def extract_posts_from_profile_html(profile_html: str) -> list[SourcePost]:
  """
  Extract individual carousel items from the recruiter profile HTML.

  Current implementation:
  1. take the full recruiter profile HTML,
  2. isolate the post carousel HTML,
  3. split each direct `li` child into a SourcePost with both HTML and text.
  4. keep only the first twelve hydrated posts, which is enough to cover the
     currently observed carousel items without depending on a stricter selector.

  A later LLM step can operate on each individual `SourcePost.html` blob rather
  than the full page HTML.
  """
  carousel_html = extract_post_carousel_html(profile_html)
  soup = BeautifulSoup(carousel_html, "html.parser")
  carousels = _require_carousel_candidates(soup)

  posts: list[SourcePost] = []
  for carousel in carousels:
    for item in carousel.find_all("li", recursive=False):
      post_html = str(item)
      post_text = _extract_post_text(item)
      post_url = _extract_post_url(item)
      post_id = _extract_post_id(post_url)

      if not post_html.strip() or not post_text.strip():
        continue

      posts.append(
        SourcePost(
          linkedin_post_id=post_id,
          url=post_url,
          text=post_text,
          html=post_html,
        )
      )

  return posts[:HYDRATED_POST_LIMIT]
