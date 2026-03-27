# Backend Debugging

Utilities in this folder let you exercise pieces of the LinkedIn crawler
pipeline without waiting for cron.

Run all commands from the project root:

```bash
cd /Users/liu21d/Documents/Code/TalentSync
```

Make sure `backend/.env` is populated first, especially:

- `DATABASE_URL`
- `OPENAI_API_KEY`
- `LINKEDIN_COOKIE_LI_AT`

## Run The Crawler Immediately

Uses the real `backend.crawler_main` pipeline, but triggers it on demand.

Run the current host-machine hour, matching cron behavior:

```bash
python -m backend.debugging.run_crawler_now
```

Run a specific slot:

```bash
python -m backend.debugging.run_crawler_now --slot 14
```

Run all 24 slots, useful when you want to exercise the full recruiter table:

```bash
python -m backend.debugging.run_crawler_now --all-slots
```

This creates `job_runs` entries with the job name `debug_hourly_recruiter_crawl`.

## Save A Rendered LinkedIn Snapshot

Uses Selenium plus the `li_at` cookie to load the hardcoded profile and save the
fully rendered HTML and a screenshot.

```bash
python -m backend.debugging.linkedin_rendered_snapshot
```

Outputs:

- `backend/debugging/linkedin_gkangj_rendered.html`
- `backend/debugging/linkedin_gkangj_rendered.png`

## Save A Raw Cookie-Based HTML Fetch

Uses a plain HTTP request with the `li_at` cookie. This is lighter weight than
Selenium and useful for quick comparisons.

```bash
python -m backend.debugging.linkedin_cookie_fetch
```

Output:

- `backend/debugging/linkedin_gkangj.html`

## Run The Parser On A Saved HTML File

Uses the real parser on a local rendered HTML file and writes out the extracted
carousel HTML plus one HTML file per parsed carousel item.

Current limitation: the parser currently keeps up to 12 hydrated carousel items
from the rendered LinkedIn HTML. This is intentionally broader than a
single-carousel selector so we can keep the HTML matching logic less brittle.

Run against the default saved snapshot:

```bash
python -m backend.debugging.run_parser_on_saved_html
```

Run against a specific HTML file:

```bash
python -m backend.debugging.run_parser_on_saved_html backend/debugging/linkedin_gkangj_rendered.html
```

Outputs:

- `backend/debugging/parser_output/carousel.html`
- `backend/debugging/parser_output/posts/post_01.html` and so on
- `backend/debugging/parser_output/summary.json`

## Notes

- Prefer the Selenium snapshot when you need rendered LinkedIn content such as
  the carousel.
- `backend.crawler_main` now saves the fetched rendered profile HTML into
  `backend/debugging/linkedin_gkangj_rendered.html` before parsing, so you can
  inspect exactly what the crawler saw when debugging parser failures.
- Prefer `run_parser_on_saved_html` when you want to confirm whether the parser
  can find and split the carousel in a saved rendered page.
- Prefer `run_crawler_now` when you want to test the end-to-end pipeline
  including DB writes, parsing, classification, and dedupe.
- Prefer the raw cookie fetch when you only want to compare the server response
  with the rendered browser output.
