from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "order" ALTER COLUMN "delivery_date" DROP NOT NULL;
        ALTER TABLE "order" ALTER COLUMN "params" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "order" ALTER COLUMN "delivery_date" SET NOT NULL;
        ALTER TABLE "order" ALTER COLUMN "params" SET NOT NULL;"""
