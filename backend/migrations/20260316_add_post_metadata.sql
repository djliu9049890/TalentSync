ALTER TABLE posts
  ADD COLUMN IF NOT EXISTS job_title text,
  ADD COLUMN IF NOT EXISTS company text,
  ADD COLUMN IF NOT EXISTS location text,
  ADD COLUMN IF NOT EXISTS employment_type text,
  ADD COLUMN IF NOT EXISTS experience_level text,
  ADD COLUMN IF NOT EXISTS skills text[],
  ADD COLUMN IF NOT EXISTS salary text,
  ADD COLUMN IF NOT EXISTS hiring_contact_name text,
  ADD COLUMN IF NOT EXISTS hiring_contact_linkedin_url text,
  ADD COLUMN IF NOT EXISTS extraction_payload jsonb;
