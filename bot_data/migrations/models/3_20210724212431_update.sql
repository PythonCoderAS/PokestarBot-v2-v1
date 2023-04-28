-- upgrade --
ALTER TABLE "argument" ALTER COLUMN "name" TYPE VARCHAR(128) USING "name"::VARCHAR(128);
ALTER TABLE "command" ALTER COLUMN "name" TYPE VARCHAR(128) USING "name"::VARCHAR(128);
ALTER TABLE "example" ALTER COLUMN "code" TYPE VARCHAR(128) USING "code"::VARCHAR(128);
CREATE TABLE IF NOT EXISTS "slashcommand" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "option_list" JSONB NOT NULL DEFAULT '[]'::JSONB,
    "command_id" INT NOT NULL REFERENCES "command" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_slashcomman_name_394db5" UNIQUE ("name", "option_list")
);
CREATE INDEX IF NOT EXISTS "idx_slashcomman_name_42f690" ON "slashcommand" ("name");;
-- downgrade --
ALTER TABLE "command" ALTER COLUMN "name" TYPE VARCHAR(2000) USING "name"::VARCHAR(2000);
ALTER TABLE "example" ALTER COLUMN "code" TYPE VARCHAR(2000) USING "code"::VARCHAR(2000);
ALTER TABLE "argument" ALTER COLUMN "name" TYPE VARCHAR(2000) USING "name"::VARCHAR(2000);
DROP TABLE IF EXISTS "slashcommand";
