-- upgrade --
CREATE TABLE IF NOT EXISTS "invite" (
    "guild_id" BIGINT NOT NULL,
    "code" VARCHAR(16) NOT NULL PRIMARY KEY,
    "uses" INT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_invite_guild_i_886855" ON "invite" ("guild_id");
-- downgrade --
DROP TABLE IF EXISTS "invite";
