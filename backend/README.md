# TalentSync Backend (Crawler DB)

This folder contains the database layer for the crawler that ingests recruiter posts.

## 1. Requirements

- Python 3.11+ (recommended)
- A running Postgres instance

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

## 3. Creating the schema

Make sure Postgres is running and the target database already exists, then run (from project root):

```bash
python -m backend.init_db
```

This will create (if they do not already exist):

- `recruiters` table
- `posts` table

These tables include uniqueness constraints for post deduplication based on:

- `linkedin_post_id`
- `linkedin_post_url`
