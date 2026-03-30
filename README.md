# TalentSync

TalentSync is a recruiter-post-powered job board. The frontend is a Next.js job
board prototype, and the backend is a Python crawler pipeline that fetches
LinkedIn recruiter profiles, parses recent post carousel items, classifies job
posts with OpenAI, and stores them in Postgres / Supabase.

## Repo stack

### Frontend

- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- **Tailwind CSS**
- **lucide-react**

### Backend

- **Python 3.11+**
- **SQLAlchemy**
- **Postgres / Supabase**
- **Selenium + Chrome**
- **OpenAI Responses API**

## Frontend local development

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Frontend production build

```bash
npm run build
npm start
```

## Backend overview

The backend lives in `backend/` and currently includes:

- an hourly crawler: `python -m backend.crawler_main`
- a nightly cleanup job: `python -m backend.maintenance`
- SQLAlchemy models for `recruiters`, `posts`, and `job_runs`
- Selenium-based LinkedIn profile fetching using a `li_at` cookie
- HTML parsing for LinkedIn carousel items
- OpenAI-based job post classification and metadata extraction

Current crawler flow:

1. Select recruiters whose `crawl_slot_hour` matches the current hour.
2. Fetch the recruiter's LinkedIn profile HTML with Selenium.
3. Parse hydrated carousel items into individual post fragments.
4. Classify each post with OpenAI.
5. Dedupe job posts and insert new rows into `posts`.
6. Record run results in `job_runs`.

For backend setup, env vars, migrations, and debug commands, see
`backend/README.md` and `backend/debugging/README.md`.

## Repo structure

- `src/app/` - Next.js app router files
- `src/components/` - frontend UI components
- `src/data/mockJobs.ts` - mock frontend data
- `backend/` - crawler, database, parsing, classification, and debug tooling
