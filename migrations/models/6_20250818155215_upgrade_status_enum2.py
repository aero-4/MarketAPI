from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "payment" DROP COLUMN "currency";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "payment" ADD "currency" VARCHAR(8) NOT NULL DEFAULT 'RUB';"""
