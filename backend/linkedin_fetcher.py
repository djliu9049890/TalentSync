from __future__ import annotations

import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .config import (
  get_linkedin_cookie_li_at,
  get_linkedin_headless,
  get_linkedin_page_load_timeout,
  get_linkedin_post_load_scrolls,
  get_linkedin_wait_timeout,
)

LINKEDIN_HOME_URL = "https://www.linkedin.com"


def build_driver() -> WebDriver:
  options = Options()
  options.add_argument("--window-size=1440,2200")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")

  if get_linkedin_headless():
    options.add_argument("--headless=new")

  service = Service()
  driver = webdriver.Chrome(service=service, options=options)
  driver.set_page_load_timeout(get_linkedin_page_load_timeout())
  return driver


def inject_cookie(driver: WebDriver) -> None:
  li_at = get_linkedin_cookie_li_at()
  if not li_at:
    raise RuntimeError("LINKEDIN_COOKIE_LI_AT is not set.")

  driver.get(LINKEDIN_HOME_URL)
  driver.add_cookie(
    {
      "name": "li_at",
      "value": li_at,
      "domain": ".linkedin.com",
      "path": "/",
      "secure": True,
      "httpOnly": True,
    }
  )


def wait_for_profile_page(driver: WebDriver) -> None:
  WebDriverWait(driver, get_linkedin_wait_timeout()).until(
    EC.presence_of_element_located(("tag name", "body"))
  )
  WebDriverWait(driver, get_linkedin_wait_timeout()).until(
    lambda current_driver: current_driver.execute_script(
      "return document.readyState"
    ) == "complete"
  )


def warm_profile_page(driver: WebDriver) -> None:
  scrolls = max(get_linkedin_post_load_scrolls(), 0)
  for _ in range(scrolls):
    driver.execute_script("window.scrollBy(0, 900);")
    time.sleep(1.5)
  driver.execute_script("window.scrollTo(0, 0);")
  time.sleep(0.5)


def fetch_profile_html(profile_url: str) -> str:
  driver = build_driver()
  try:
    inject_cookie(driver)
    driver.get(profile_url)
    wait_for_profile_page(driver)
    warm_profile_page(driver)
    return driver.page_source
  except TimeoutException as exc:
    raise RuntimeError(f"Timed out loading LinkedIn profile page: {profile_url}") from exc
  finally:
    driver.quit()
