-- upgrade --
CREATE TABLE IF NOT EXISTS "anime" (
    "name" VARCHAR(2000) NOT NULL  PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "animealias" (
    "alias" VARCHAR(2000) NOT NULL  PRIMARY KEY,
    "anime_id" VARCHAR(2000) NOT NULL REFERENCES "anime" ("name") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "blockedprivatechannel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "channel_id" BIGINT NOT NULL,
    "author_id" BIGINT NOT NULL,
    CONSTRAINT "uid_blockedpriv_channel_0a98d6" UNIQUE ("channel_id", "author_id")
);
CREATE INDEX IF NOT EXISTS "idx_blockedpriv_channel_58e5b2" ON "blockedprivatechannel" ("channel_id");
CREATE INDEX IF NOT EXISTS "idx_blockedpriv_author__4b5f18" ON "blockedprivatechannel" ("author_id");
CREATE TABLE IF NOT EXISTS "botspamcommand" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "name" VARCHAR(2000) NOT NULL,
    CONSTRAINT "uid_botspamcomm_guild_i_fa5ebb" UNIQUE ("guild_id", "name")
);
CREATE INDEX IF NOT EXISTS "idx_botspamcomm_guild_i_5e69dd" ON "botspamcommand" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_botspamcomm_name_3bf8e3" ON "botspamcommand" ("name");
CREATE TABLE IF NOT EXISTS "bracket" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "author_id" BIGINT NOT NULL,
    "name" VARCHAR(2000) NOT NULL,
    "status" SMALLINT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_bracket_guild_i_a08586" ON "bracket" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_bracket_author__ee831e" ON "bracket" ("author_id");
COMMENT ON COLUMN "bracket"."status" IS 'OPEN: 1\nVOTABLE: 2\nCLOSED: 3\nLOCKED: 4';
CREATE TABLE IF NOT EXISTS "command" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(2000) NOT NULL UNIQUE,
    "description" TEXT
);
CREATE INDEX IF NOT EXISTS "idx_command_name_a5f5d3" ON "command" ("name");
CREATE TABLE IF NOT EXISTS "argument" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(2000),
    "description" TEXT NOT NULL,
    "order" SMALLINT NOT NULL,
    "optional" BOOL NOT NULL  DEFAULT False,
    "repeatable" BOOL NOT NULL  DEFAULT False,
    "command_id" INT NOT NULL REFERENCES "command" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_argument_command_88129f" UNIQUE ("command_id", "name"),
    CONSTRAINT "uid_argument_command_b35c80" UNIQUE ("command_id", "order")
);
CREATE INDEX IF NOT EXISTS "idx_argument_order_953954" ON "argument" ("order");
CREATE TABLE IF NOT EXISTS "disabledcommand" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "name" VARCHAR(2000) NOT NULL,
    CONSTRAINT "uid_disabledcom_guild_i_fcfad6" UNIQUE ("guild_id", "name")
);
CREATE INDEX IF NOT EXISTS "idx_disabledcom_guild_i_e2eac2" ON "disabledcommand" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_disabledcom_name_0a14e9" ON "disabledcommand" ("name");
CREATE TABLE IF NOT EXISTS "example" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code" VARCHAR(2000) NOT NULL,
    "text" TEXT NOT NULL,
    "argument_id" INT NOT NULL REFERENCES "argument" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_example_argumen_ec0c03" UNIQUE ("argument_id", "code")
);
CREATE TABLE IF NOT EXISTS "globaloption" (
    "name" VARCHAR(256) NOT NULL  PRIMARY KEY,
    "value" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "invite" (
    "guild_id" BIGINT NOT NULL,
    "code" VARCHAR(6) NOT NULL  PRIMARY KEY,
    "uses" INT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_invite_guild_i_886855" ON "invite" ("guild_id");
CREATE TABLE IF NOT EXISTS "namedchannel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "channel_id" BIGINT NOT NULL,
    "channel_name" VARCHAR(64) NOT NULL,
    CONSTRAINT "uid_namedchanne_guild_i_92da77" UNIQUE ("guild_id", "channel_name")
);
CREATE INDEX IF NOT EXISTS "idx_namedchanne_guild_i_4290dd" ON "namedchannel" ("guild_id");
CREATE TABLE IF NOT EXISTS "namedrole" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "role_id" BIGINT NOT NULL,
    "role_name" VARCHAR(64) NOT NULL,
    CONSTRAINT "uid_namedrole_guild_i_2ef2ed" UNIQUE ("guild_id", "role_name")
);
CREATE INDEX IF NOT EXISTS "idx_namedrole_guild_i_291201" ON "namedrole" ("guild_id");
CREATE TABLE IF NOT EXISTS "option" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "name" VARCHAR(1990) NOT NULL,
    "enabled" BOOL NOT NULL  DEFAULT True,
    CONSTRAINT "uid_option_guild_i_1a4f63" UNIQUE ("guild_id", "name")
);
CREATE INDEX IF NOT EXISTS "idx_option_guild_i_cab4ac" ON "option" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_option_name_abe08f" ON "option" ("name");
CREATE TABLE IF NOT EXISTS "prefix" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "value" VARCHAR(20) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_prefix_guild_i_22997b" ON "prefix" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_prefix_value_3efe4f" ON "prefix" ("value");
CREATE TABLE IF NOT EXISTS "privatechannel" (
    "channel_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "author_id" BIGINT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_privatechan_author__e464b0" ON "privatechannel" ("author_id");
CREATE TABLE IF NOT EXISTS "rolesnapshot" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "author_id" BIGINT NOT NULL,
    "role_id" BIGINT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_rolesnapsho_guild_i_9e58a9" ON "rolesnapshot" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_rolesnapsho_role_id_f0b3ea" ON "rolesnapshot" ("role_id");
CREATE TABLE IF NOT EXISTS "socialprofileitem" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT,
    "author_id" BIGINT NOT NULL,
    "name" VARCHAR(128) NOT NULL,
    "value" VARCHAR(1024) NOT NULL,
    CONSTRAINT "uid_socialprofi_guild_i_3763e8" UNIQUE ("guild_id", "author_id", "name")
);
CREATE INDEX IF NOT EXISTS "idx_socialprofi_author__7f3e83" ON "socialprofileitem" ("author_id");
CREATE INDEX IF NOT EXISTS "idx_socialprofi_name_ff1f99" ON "socialprofileitem" ("name");
CREATE TABLE IF NOT EXISTS "stat" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "channel_id" BIGINT NOT NULL,
    "author_id" BIGINT NOT NULL,
    "NUM" INT NOT NULL,
    CONSTRAINT "uid_stat_guild_i_be8c4e" UNIQUE ("guild_id", "channel_id", "author_id")
);
CREATE INDEX IF NOT EXISTS "idx_stat_guild_i_2e7d6e" ON "stat" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_stat_channel_0e34cb" ON "stat" ("channel_id");
CREATE INDEX IF NOT EXISTS "idx_stat_author__6cc80f" ON "stat" ("author_id");
CREATE TABLE IF NOT EXISTS "usersnapshot" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "author_id" BIGINT NOT NULL,
    "role_id" BIGINT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_usersnapsho_guild_i_8808e5" ON "usersnapshot" ("guild_id");
CREATE INDEX IF NOT EXISTS "idx_usersnapsho_author__6c6e7b" ON "usersnapshot" ("author_id");
CREATE TABLE IF NOT EXISTS "waifu" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(2000) NOT NULL UNIQUE,
    "description" VARCHAR(2048) NOT NULL,
    "image" VARCHAR(1024) NOT NULL UNIQUE,
    "anime_id" VARCHAR(2000) NOT NULL REFERENCES "anime" ("name") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "bracketwaifu" (
    "rank" SERIAL NOT NULL PRIMARY KEY,
    "bracket_id" INT NOT NULL REFERENCES "bracket" ("id") ON DELETE CASCADE,
    "waifu_id" INT NOT NULL REFERENCES "waifu" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "vote" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "author_id" BIGINT NOT NULL,
    "bracket_waifu_id" INT NOT NULL REFERENCES "bracketwaifu" ("rank") ON DELETE CASCADE,
    CONSTRAINT "uid_vote_author__64a0b3" UNIQUE ("author_id", "bracket_waifu_id")
);
CREATE INDEX IF NOT EXISTS "idx_vote_author__463514" ON "vote" ("author_id");
CREATE TABLE IF NOT EXISTS "waifualias" (
    "alias" VARCHAR(2000) NOT NULL  PRIMARY KEY,
    "waifu_id" INT NOT NULL REFERENCES "waifu" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
