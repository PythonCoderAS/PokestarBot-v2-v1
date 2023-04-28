-- upgrade --
CREATE TABLE IF NOT EXISTS "markdownpage" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "title" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "modtime" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
-- downgrade --
DROP TABLE IF EXISTS "markdownpage";
