from __future__ import annotations

from pathlib import Path

PROFILE_URL = "https://www.linkedin.com/in/gkangj"
BASE_DIR = Path(__file__).resolve().parent
HTML_OUTPUT_PATH = BASE_DIR / "linkedin_gkangj_rendered.html"
SCREENSHOT_OUTPUT_PATH = BASE_DIR / "linkedin_gkangj_rendered.png"

from .linkedin_fetcher import build_driver, inject_cookie, wait_for_profile_page, warm_profile_page


def main() -> None:
  driver = build_driver()

  try:
    inject_cookie(driver)
    driver.get(PROFILE_URL)
    wait_for_profile_page(driver)
    warm_profile_page(driver)

    rendered_html = driver.page_source
    HTML_OUTPUT_PATH.write_text(rendered_html, encoding="utf-8")
    driver.save_screenshot(str(SCREENSHOT_OUTPUT_PATH))

    print(f"Saved rendered HTML to {HTML_OUTPUT_PATH}")
    print(f"Saved screenshot to {SCREENSHOT_OUTPUT_PATH}")
    print(f"Final URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
  finally:
    driver.quit()


if __name__ == "__main__":
  main()
