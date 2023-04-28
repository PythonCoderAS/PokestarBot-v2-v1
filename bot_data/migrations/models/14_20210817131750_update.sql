-- upgrade --
CREATE TABLE IF NOT EXISTS "hiddenstatisticchannel" (
    "guild_id" BIGINT NOT NULL,
    "channel_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "child_channel_id" BIGINT,
    CONSTRAINT "uid_hiddenstati_guild_i_17d5a0" UNIQUE ("guild_id", "channel_id", "child_channel_id")
);
CREATE INDEX IF NOT EXISTS "idx_hiddenstati_guild_i_8a9b1d" ON "hiddenstatisticchannel" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_hiddenstati_child_c_131fe7" ON "hiddenstatisticchannel" ("child_channel_id");;
CREATE TABLE IF NOT EXISTS "statschannel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "channel_id" BIGINT NOT NULL,
    "child_channel_id" BIGINT,
    CONSTRAINT "uid_statschanne_guild_i_67edac" UNIQUE ("guild_id", "channel_id", "child_channel_id")
);
CREATE INDEX IF NOT EXISTS "idx_statschanne_guild_i_33faa7" ON "statschannel" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_statschanne_channel_ce49e7" ON "statschannel" ("channel_id");
CREATE INDEX IF NOT EXISTS "idx_statschanne_child_c_664be0" ON "statschannel" ("child_channel_id");;
CREATE TABLE IF NOT EXISTS "statistic" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "author_id" BIGINT NOT NULL,
    "NUM" INT NOT NULL,
    "parent_channel_id" INT NOT NULL REFERENCES "statschannel" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_statistic_parent__6cd2fa" UNIQUE ("parent_channel_id", "author_id")
);
CREATE INDEX IF NOT EXISTS "idx_statistic_author__789272" ON "statistic" ("author_id");;
-- downgrade --
DROP TABLE IF EXISTS "hiddenstatisticchannel";
DROP TABLE IF EXISTS "statistic";
DROP TABLE IF EXISTS "statschannel";
