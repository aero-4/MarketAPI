from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "media" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "group_id" UUID,
    "url" VARCHAR(512) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_media_group_i_8fe404" ON "media" ("group_id");
CREATE TABLE IF NOT EXISTS "attachment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content_type" VARCHAR(50) NOT NULL,
    "object_id_int" INT,
    "object_id_uuid" UUID,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "media_id" INT NOT NULL REFERENCES "media" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_attachment_content_1c46ee" ON "attachment" ("content_type", "object_id_int");
CREATE INDEX IF NOT EXISTS "idx_attachment_content_9c3f65" ON "attachment" ("content_type", "object_id_uuid");
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(64),
    "full_name" VARCHAR(64),
    "photo" TEXT,
    "email" VARCHAR(128),
    "phone" BIGINT,
    "role" INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "question" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "article_id" INT NOT NULL,
    "date_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "text" VARCHAR(512) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "item" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_visible" BOOL NOT NULL DEFAULT False,
    "article_id" BIGINT NOT NULL,
    "title" VARCHAR(512),
    "slug" VARCHAR(512) NOT NULL,
    "description" TEXT NOT NULL,
    "price" INT NOT NULL DEFAULT 0,
    "discount_price" INT NOT NULL DEFAULT 0,
    "cat" VARCHAR(128) NOT NULL,
    "sub_cat" VARCHAR(128) NOT NULL,
    "params" JSONB NOT NULL,
    "rating" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "count_all" INT NOT NULL DEFAULT 0,
    "seller_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "review" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "content" VARCHAR(512) NOT NULL,
    "grade" INT NOT NULL,
    "item_id" INT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE,
    "media_id" INT REFERENCES "media" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "wish" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "catеgory" VARCHAR(128),
    "item_id" INT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "likes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "current_id" INT NOT NULL UNIQUE,
    "object_type" VARCHAR(19) NOT NULL,
    "value" INT NOT NULL,
    "item_id" INT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "likes"."object_type" IS 'REVIEW_LIKE: review-like\nREVIEW_REPLY_LIKE: review-reply-like\nQUESTION_LIKE: question-like\nQUESTION_REPLY_LIKE: question-reply-like';
CREATE TABLE IF NOT EXISTS "refreshtoken" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "jti" VARCHAR(64) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "revoked" BOOL NOT NULL DEFAULT False,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_refreshtoke_jti_708583" ON "refreshtoken" ("jti");
CREATE TABLE IF NOT EXISTS "replies" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "current_id" INT NOT NULL,
    "object_type" VARCHAR(14) NOT NULL,
    "content" VARCHAR(256) NOT NULL,
    "item_id" INT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "replies"."object_type" IS 'REVIEW_REPLY: review-reply\nREVIEW: review\nQUESTION_REPLY: question-reply\nQUESTION: question';
CREATE TABLE IF NOT EXISTS "useraddress" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "address" VARCHAR(512) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
