from __future__ import annotations

import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROFILE_URL = "https://www.linkedin.com/in/gkangj"
OUTPUT_PATH = Path(__file__).resolve().parent / "linkedin_gkangj.html"
ENV_PATH = Path(__file__).resolve().parent / ".env"


def load_local_env() -> None:
  if not ENV_PATH.exists():
    return

  for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if not line or line.startswith("#") or "=" not in line:
      continue
    key, value = line.split("=", 1)
    os.environ.setdefault(key.strip(), value.strip())


def build_request() -> Request:
  load_local_env()
  li_at = os.getenv("LINKEDIN_COOKIE_LI_AT")
  if not li_at:
    raise RuntimeError("LINKEDIN_COOKIE_LI_AT is not set in backend/.env")

  headers = {
    "User-Agent": (
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": (
      "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
      "image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cookie": f"li_at={li_at}",
  }
  return Request(PROFILE_URL, headers=headers)


def main() -> None:
  request = build_request()
  try:
    with urlopen(request, timeout=30) as response:
      html = response.read().decode("utf-8", errors="replace")
      OUTPUT_PATH.write_text(html, encoding="utf-8")
      print(f"Saved HTML to {OUTPUT_PATH}")
      print(f"HTTP status: {response.status}")
      print(f"Final URL: {response.geturl()}")
  except HTTPError as exc:
    body = exc.read().decode("utf-8", errors="replace")
    OUTPUT_PATH.write_text(body, encoding="utf-8")
    print(f"Saved error HTML to {OUTPUT_PATH}")
    print(f"HTTP status: {exc.code}")
    print(f"Final URL: {exc.geturl()}")
    raise
  except URLError as exc:
    raise RuntimeError(f"Failed to fetch LinkedIn profile: {exc.reason}") from exc


if __name__ == "__main__":
  main()
