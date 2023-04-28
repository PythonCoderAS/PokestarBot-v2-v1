-- upgrade --
CREATE TABLE IF NOT EXISTS "statschannel" (
    "guild_id" BIGINT NOT NULL,
    "channel_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "parent_channel_id" BIGINT REFERENCES "statschannel" ("channel_id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_statschanne_guild_i_33faa7" ON "statschannel" ("guild_id");;
CREATE TABLE IF NOT EXISTS "hiddenstatisticchannel" (
    "guild_id" BIGINT NOT NULL,
    "channel_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "parent_channel_id" BIGINT REFERENCES "hiddenstatisticchannel" ("channel_id") ON DELETE CASCADE,
    CONSTRAINT "uid_hiddenstati_guild_i_ecdb4d" UNIQUE ("guild_id", "channel_id")
);
CREATE INDEX IF NOT EXISTS "idx_hiddenstati_guild_i_8a9b1d" ON "hiddenstatisticchannel" ("guild_id");;
CREATE TABLE IF NOT EXISTS "statistic" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "author_id" BIGINT NOT NULL,
    "NUM" INT NOT NULL,
    "parent_channel_id" BIGINT NOT NULL REFERENCES "statschannel" ("channel_id") ON DELETE CASCADE,
    CONSTRAINT "uid_statistic_parent__6cd2fa" UNIQUE ("parent_channel_id", "author_id")
);
CREATE INDEX IF NOT EXISTS "idx_statistic_author__789272" ON "statistic" ("author_id");;
-- downgrade --
DROP TABLE IF EXISTS "hiddenstatisticchannel";
DROP TABLE IF EXISTS "statistic";
DROP TABLE IF EXISTS "statschannel";
