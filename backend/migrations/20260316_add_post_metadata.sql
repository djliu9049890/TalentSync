ALTER TABLE posts
  ADD COLUMN IF NOT EXISTS job_title text,
  ADD COLUMN IF NOT EXISTS company text,
  ADD COLUMN IF NOT EXISTS location text,
  ADD COLUMN IF NOT EXISTS employment_type text,
  ADD COLUMN IF NOT EXISTS salary text,
  ADD COLUMN IF NOT EXISTS hiring_contact text,
  ADD COLUMN IF NOT EXISTS extraction_payload jsonb;
