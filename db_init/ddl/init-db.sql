-- Link to schema: https://app.quickdatabasediagrams.com/#/d/IZC3P0
CREATE TABLE IF NOT EXISTS "Channels" (
    "channel_id" bigint NOT NULL,
    "title" text NOT NULL,
    "link" text NOT NULL,
    "about" text NOT NULL,
    -- with timezone
    "date" time with time zone NOT NULL,
    "participants_count" int NOT NULL,
    -- default 0
    "total_photos" int NOT NULL DEFAULT 0,
    -- default 0
    "total_video" int NOT NULL DEFAULT 0,
    -- default 0
    "total_document" int NOT NULL DEFAULT 0,
    -- default 0
    "total_music" int NOT NULL DEFAULT 0,
    -- default 0
    "total_url" int NOT NULL DEFAULT 0,
    -- default 0
    "total_voice" int NOT NULL DEFAULT 0,
    -- default 0
    "total_gif" int NOT NULL DEFAULT 0,
    CONSTRAINT "pk_channels" PRIMARY KEY ("channel_id")
);

CREATE TABLE IF NOT EXISTS "Messages" (
    "message_id" bigint NOT NULL,
    "channel_id" bigint NOT NULL,
    "message" text NOT NULL,
    -- with time
    "date" time with time zone NOT NULL,
    "views" int NOT NULL,
    "forwards" int NOT NULL DEFAULT 0,
    -- default 0
    "replies_cnt" int NOT NULL DEFAULT 0,
    "fwd_from_channel_id" bigint NULL,
    "fwd_from_message_id" bigint NULL,
    CONSTRAINT "pk_messages" PRIMARY KEY ("message_id", "channel_id"),
    FOREIGN KEY ("channel_id") REFERENCES "Channels" ("channel_id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "Replies" (
    "id" bigint NOT NULL,
    "message_id" bigint NOT NULL,
    "channel_id" bigint NOT NULL,
    "message" text NOT NULL,
    -- with timezone
    "date" time with time zone NOT NULL,
    "user_id" bigint NOT NULL,
    CONSTRAINT "pk_replies" PRIMARY KEY ("id"),
    FOREIGN KEY ("message_id", "channel_id") REFERENCES "Messages" ("message_id", "channel_id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "UserChannel" (
    -- complex primary key
    "channel_id" bigint NOT NULL,
    "user_id" bigint NOT NULL,
    "is_bot" bool DEFAULT false,
    "username" text NULL,
    CONSTRAINT "pk_UserChannel" PRIMARY KEY ("channel_id", "user_id"),
    FOREIGN KEY ("channel_id") REFERENCES "Channels" ("channel_id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "ChannelRelation"(
    "from_channel_link" TEXT NOT NULL,
    "to_channel_link" TEXT NOT NULL,
    CONSTRAINT "pk_ChannelRelation" PRIMARY KEY ("from_channel_link", "to_channel_link")
);

DO $$ BEGIN IF NOT EXISTS (
    SELECT
        1
    FROM
        pg_type
    WHERE
        typname = 'processing_status'
) THEN CREATE TYPE processing_status AS ENUM ('ok', 'error', 'processing', 'to_process');

END IF;

END $$;

CREATE TABLE IF NOT EXISTS "ChannelQueue" (
    "link" TEXT NOT NULL,
    -- enum ok, error, to_process, processing
    "status" processing_status NOT NULL DEFAULT 'to_process',
    CONSTRAINT "pk_ChannelQueue" PRIMARY KEY ("link")
);