-- upgrade --
ALTER TABLE "command" ALTER COLUMN "description" SET DEFAULT '**This command was generated automatically. Please replace this message with an actual description.**';
ALTER TABLE "command" ALTER COLUMN "description" SET NOT NULL;
ALTER TABLE "example" ALTER COLUMN "text" SET DEFAULT '**This example was generated automatically. Please replace this message with an actual description.**';
-- downgrade --
ALTER TABLE "command" ALTER COLUMN "description" DROP NOT NULL;
ALTER TABLE "command" ALTER COLUMN "description" DROP DEFAULT;
ALTER TABLE "example" ALTER COLUMN "text" DROP DEFAULT;
