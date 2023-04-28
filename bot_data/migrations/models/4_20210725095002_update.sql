-- upgrade --
CREATE TABLE IF NOT EXISTS "commandusage" (
    "guild_id" BIGINT,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "day" DATE NOT NULL,
    "command" VARCHAR(128) NOT NULL,
    "slash" BOOL NOT NULL  DEFAULT False,
    "count" INT NOT NULL  DEFAULT 0,
    CONSTRAINT "uid_commandusag_guild_i_0ac2b5" UNIQUE ("guild_id", "day", "command", "slash")
);
CREATE INDEX IF NOT EXISTS "idx_commandusag_guild_i_2d5555" ON "commandusage" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_commandusag_slash_566d82" ON "commandusage" ("slash");;
CREATE TABLE IF NOT EXISTS "genericbotstat" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT,
    "type" VARCHAR(64) NOT NULL,
    "day" DATE NOT NULL,
    "count" INT NOT NULL  DEFAULT 0,
    CONSTRAINT "uid_genericbots_guild_i_6544a9" UNIQUE ("guild_id", "day", "type")
);
CREATE INDEX IF NOT EXISTS "idx_genericbots_guild_i_5ed722" ON "genericbotstat" ("guild_id");;
-- downgrade --
DROP TABLE IF EXISTS "commandusage";
DROP TABLE IF EXISTS "genericbotstat";
