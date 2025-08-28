from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "payment" ADD "user_id" INT NOT NULL;
        ALTER TABLE "order" ALTER COLUMN "status" TYPE VARCHAR(2) USING "status"::VARCHAR(2);
        ALTER TABLE "payment" ADD CONSTRAINT "fk_payment_user_3d4ede6e" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "payment" DROP CONSTRAINT IF EXISTS "fk_payment_user_3d4ede6e";
        ALTER TABLE "order" ALTER COLUMN "status" TYPE SMALLINT USING "status"::SMALLINT;
        ALTER TABLE "payment" DROP COLUMN "user_id";"""
