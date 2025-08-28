from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "order" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "params" JSONB NOT NULL,
    "status" SMALLINT NOT NULL,
    "delivery_date" DATE NOT NULL,
    "item_id" INT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "order"."status" IS 'CLOSED: -1\nIN_CART: 0\nWAITING: 1\nCONFIRM: 2\nIN_TRANSIT: 3\nREADY: 4';
        ALTER TABLE "user" ADD "balance" INT NOT NULL DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "balance";
        DROP TABLE IF EXISTS "order";"""
