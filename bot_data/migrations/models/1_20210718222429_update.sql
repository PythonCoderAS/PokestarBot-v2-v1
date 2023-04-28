-- upgrade --
CREATE TABLE IF NOT EXISTS "imagetemplate" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT,
    "author_id" BIGINT NOT NULL,
    "name" VARCHAR(128) NOT NULL,
    "url" VARCHAR(1024) NOT NULL,
    CONSTRAINT "uid_imagetempla_guild_i_25a69e" UNIQUE ("guild_id", "author_id", "name")
);
CREATE INDEX IF NOT EXISTS "idx_imagetempla_author__a3ab61" ON "imagetemplate" ("author_id");
CREATE INDEX IF NOT EXISTS "idx_imagetempla_name_5490fa" ON "imagetemplate" ("name");
-- downgrade --
DROP TABLE IF EXISTS "imagetemplate";
