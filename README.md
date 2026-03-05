# TalentSync – Job Board (React + TypeScript + Next.js)

A clean, modern job board UI inspired by TalentSync: header with search, filter sidebar, and job listing cards. An underrated resource in recruiting is finding jobs from recruiter posts directly as the recruiter contact is directly available for you to dm on LinkedIn. Obviously you can't follow every recruiter in the world. TalentSync collects a group of known recruiters and adds jobs to a job pool whenever a recruiters in the pool posts.

## Stack

- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- **Tailwind CSS**
- **lucide-react** (icons)

## Run locally

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Build

```bash
npm run build
npm start
```

## Structure

- `src/app/` – App router: `layout.tsx`, `page.tsx`, `globals.css`
- `src/components/` – `Header`, `Sidebar`, `JobList`, `JobCard`
- `src/data/mockJobs.ts` – Mock jobs, recruiters, and filter options

Replace mock data with your API or CMS when ready.
