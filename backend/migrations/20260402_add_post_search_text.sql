CREATE EXTENSION IF NOT EXISTS pg_trgm;

ALTER TABLE posts
  ADD COLUMN IF NOT EXISTS search_text text;

CREATE OR REPLACE FUNCTION update_post_search_text()
RETURNS trigger AS $$
BEGIN
  NEW.search_text :=
    lower(
      coalesce(NEW.job_title, '') || ' ' ||
      coalesce(NEW.company, '') || ' ' ||
      coalesce(array_to_string(NEW.skills, ' '), '')
    );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_posts_search_text ON posts;

CREATE TRIGGER trg_posts_search_text
BEFORE INSERT OR UPDATE OF job_title, company, skills
ON posts
FOR EACH ROW
EXECUTE FUNCTION update_post_search_text();

UPDATE posts
SET search_text = lower(
  coalesce(job_title, '') || ' ' ||
  coalesce(company, '') || ' ' ||
  coalesce(array_to_string(skills, ' '), '')
);

CREATE INDEX IF NOT EXISTS idx_posts_search_text_trgm
  ON posts
  USING gin (search_text gin_trgm_ops);
