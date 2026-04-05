ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "public_read_posts" ON posts;

CREATE POLICY "public_read_posts"
ON posts
FOR SELECT
TO anon, authenticated
USING (true);
