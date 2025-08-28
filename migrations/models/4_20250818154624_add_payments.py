from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "payment" (
    "id" VARCHAR(64) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "amount" DECIMAL(10,2) NOT NULL,
    "currency" VARCHAR(8) NOT NULL DEFAULT 'RUB',
    "provider_id" VARCHAR(128),
    "idempotency_key" VARCHAR(128) UNIQUE,
    "status" VARCHAR(32) NOT NULL DEFAULT 'pending',
    "order_id" INT REFERENCES "order" ("id") ON DELETE CASCADE
);
        ALTER TABLE "order" ADD "update_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "order" ALTER COLUMN "date_at" TYPE TIMESTAMPTZ USING "date_at"::TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "order" DROP COLUMN "update_at";
        ALTER TABLE "order" ALTER COLUMN "date_at" TYPE TIMESTAMPTZ USING "date_at"::TIMESTAMPTZ;
        DROP TABLE IF EXISTS "payment";"""
