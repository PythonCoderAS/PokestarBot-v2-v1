-- upgrade --
ALTER TABLE "argument" ADD "flag" BOOL NOT NULL  DEFAULT False;
ALTER TABLE "argument" ADD "literal_values" JSONB NOT NULL DEFAULT '[]'::JSONB;
ALTER TABLE "argument" ADD "quote_escaped" BOOL NOT NULL  DEFAULT True;
ALTER TABLE "commandusage" ADD "successful_count" INT NOT NULL DEFAULT 0;
-- downgrade --
ALTER TABLE "argument" DROP COLUMN "flag";
ALTER TABLE "argument" DROP COLUMN "literal_values";
ALTER TABLE "argument" DROP COLUMN "quote_escaped";
ALTER TABLE "commandusage" DROP COLUMN "successful_count";
