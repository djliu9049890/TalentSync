# TalentSync Backend (Crawler DB)

This folder contains the database layer for the crawler that ingests recruiter posts.

## 1. Requirements

- Python 3.11+ (recommended)
- A running Postgres instance
- Google Chrome installed locally

Install Python dependencies (from project root):

```bash
pip install -r backend/requirements.txt
```

## 2. Database configuration

The connection string is read from the `DATABASE_URL` environment variable.
The backend loads `backend/.env` automatically if it exists.

**Setup:**

1. Copy the example file and add your Supabase password:

   ```bash
   cp backend/.env.example backend/.env
   ```

2. Edit `backend/.env` and replace `YOUR_PASSWORD` with your real Supabase password.

If `DATABASE_URL` is not set, it falls back to a local Postgres URL (see `config.py`).

For LinkedIn browser access, Selenium uses the `LINKEDIN_COOKIE_LI_AT` cookie
from `backend/.env` to load authenticated profile pages.

## 3. Creating the schema

Make sure Postgres is running and the target database already exists, then run (from project root):

```bash
python -m backend.init_db
```

This will create (if they do not already exist):

- `recruiters` table
- `posts` table
- `job_runs` table

These tables include uniqueness constraints for post deduplication based on:

- `linkedin_post_id`
- `linkedin_post_url`

## 4. Existing databases

`python -m backend.init_db` creates missing tables, but it does not alter an
existing Supabase schema. If your `posts` table already exists, apply:

```bash
psql "$DATABASE_URL" -f backend/migrations/20260316_add_post_metadata.sql
```

That migration adds structured extraction columns such as `job_title`,
`company`, `location`, `employment_type`, `experience_level`, `skills`,
`salary`, `hiring_contact_name`, `hiring_contact_linkedin_url`, and
`extraction_payload`.

If you want the browser-based Supabase client to read `posts` safely with RLS
enabled, also apply:

```bash
psql "$DATABASE_URL" -f backend/migrations/20260405_enable_posts_rls.sql
```

That migration:

- enables RLS on `posts`
- allows `anon` and `authenticated` roles to `SELECT` from `posts`
- leaves writes locked down

## 5. Scheduled jobs

- `python -m backend.crawler_main` selects recruiters whose `crawl_slot_hour`
  matches the current host-machine hour, fetches the full LinkedIn profile HTML
  in Selenium, hands that HTML to the parser layer, classifies job posts, and
  records a `job_runs` summary.
- `python -m backend.maintenance` deletes posts older than 30 days and records
  the cleanup result in `job_runs`.

The fetch and HTML parsing layers are intentionally left pluggable so a
browser-based LinkedIn fetcher and an LLM-backed HTML parser can be added
without changing the scheduling or persistence flow.

Current limitation: the parser currently keeps up to 12 hydrated carousel items
from the rendered LinkedIn HTML. This is intentionally broader than a
single-carousel selector so we can keep the HTML matching logic less brittle.
