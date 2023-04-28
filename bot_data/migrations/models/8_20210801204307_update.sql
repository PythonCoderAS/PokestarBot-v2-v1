-- upgrade --
ALTER TABLE "argument"
    ALTER COLUMN "description" SET DEFAULT '**This argument was generated automatically. Please replace this message with an actual description.**';
-- downgrade --
ALTER TABLE "argument"
    ALTER COLUMN "description" DROP DEFAULT;
