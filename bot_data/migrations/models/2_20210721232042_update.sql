-- upgrade --
CREATE TABLE IF NOT EXISTS "bannedchannel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "channel_id" BIGINT NOT NULL,
    CONSTRAINT "uid_bannedchann_guild_i_3f31c7" UNIQUE ("guild_id", "channel_id")
);
CREATE INDEX IF NOT EXISTS "idx_bannedchann_guild_i_f09fd0" ON "bannedchannel" ("guild_id");;
CREATE TABLE IF NOT EXISTS "banneduser" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT,
    "channel_id" BIGINT,
    "author_id" BIGINT NOT NULL,
    CONSTRAINT "uid_banneduser_author__62c691" UNIQUE ("author_id", "guild_id", "channel_id")
);
CREATE INDEX IF NOT EXISTS "idx_banneduser_guild_i_1a1d42" ON "banneduser" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_banneduser_channel_5454b7" ON "banneduser" ("channel_id");
CREATE INDEX IF NOT EXISTS "idx_banneduser_author__3384ca" ON "banneduser" ("author_id");;
CREATE UNIQUE INDEX "uid_imagetempla_guild_i_cbe266" ON "imagetemplate" ("guild_id", "name");
ALTER TABLE "imagetemplate" DROP CONSTRAINT "uid_imagetempla_guild_i_25a69e";
CREATE INDEX "idx_imagetempla_guild_i_357f78" ON "imagetemplate" ("guild_id");
CREATE INDEX "idx_socialprofi_guild_i_e6078b" ON "socialprofileitem"
    ("guild_id");
-- downgrade --
CREATE UNIQUE INDEX "uid_imagetempla_guild_i_25a69e" ON "imagetemplate" ("guild_id", "author_id", "name");
ALTER TABLE "imagetemplate" DROP CONSTRAINT "uid_imagetempla_guild_i_cbe266";
DROP INDEX "idx_imagetempla_guild_i_357f78";
DROP INDEX "idx_socialprofi_guild_i_e6078b";
DROP TABLE IF EXISTS "bannedchannel";
DROP TABLE IF EXISTS "banneduser";
