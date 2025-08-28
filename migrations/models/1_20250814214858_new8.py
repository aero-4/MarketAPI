from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "question" RENAME COLUMN "article_id" TO "item";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "question" RENAME COLUMN "item" TO "article_id";"""
