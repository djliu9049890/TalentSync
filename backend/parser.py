from __future__ import annotations

from bs4 import BeautifulSoup, Tag

from .source_posts import SourcePost


def extract_post_carousel_html(profile_html: str) -> str:
  """
  Placeholder for isolating the post carousel from the full LinkedIn profile HTML.

  This exists as a separate step so the browser fetcher can stay dumb and
  resilient: it returns the full page HTML, and the parser layer decides how to
  narrow that down before asking an LLM to split it into posts.
  """
  soup = BeautifulSoup(profile_html, "html.parser")
  carousel = soup.find("ul", attrs={"data-testid": "carousel-children-container"})
  if carousel is None:
    raise ValueError("Could not find LinkedIn post carousel container in profile HTML.")
  return str(carousel)


def _extract_post_text(post_node: Tag) -> str:
  return post_node.get_text(" ", strip=True)


def extract_posts_from_profile_html(profile_html: str) -> list[SourcePost]:
  """
  Extract individual carousel items from the recruiter profile HTML.

  Current implementation:
  1. take the full recruiter profile HTML,
  2. isolate the post carousel HTML,
  3. split each direct `li` child into a SourcePost with both HTML and text.

  A later LLM step can operate on each individual `SourcePost.html` blob rather
  than the full page HTML.
  """
  carousel_html = extract_post_carousel_html(profile_html)
  soup = BeautifulSoup(carousel_html, "html.parser")
  carousel = soup.find("ul", attrs={"data-testid": "carousel-children-container"})
  if carousel is None:
    raise ValueError("Could not parse extracted LinkedIn post carousel HTML.")

  posts: list[SourcePost] = []
  for item in carousel.find_all(
    "li",
    attrs={"data-testid": "carousel-child-container"},
    recursive=False,
  ):
    post_html = str(item)
    post_text = _extract_post_text(item)

    if not post_html.strip() or not post_text.strip():
      continue

    posts.append(
      SourcePost(
        linkedin_post_id=None,
        url=None,
        text=post_text,
        html=post_html,
      )
    )

  return posts
