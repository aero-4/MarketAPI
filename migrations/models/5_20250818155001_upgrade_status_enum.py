from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "payment" ALTER COLUMN "status" TYPE VARCHAR(32) USING "status"::VARCHAR(32);
        COMMENT ON COLUMN "payment"."status" IS 'PENDING: pending
EXPIRED: expired
FAIL: fail
SUCCESS: success';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "payment" ALTER COLUMN "status" TYPE VARCHAR(32) USING "status"::VARCHAR(32);
        COMMENT ON COLUMN "payment"."status" IS NULL;"""
