DO $$ BEGIN IF NOT EXISTS (
    SELECT
        1
    FROM
        pg_type
    WHERE
        typname = 'channel_status'
) THEN CREATE TYPE process_status AS ENUM ('process', 'processing', 'error', 'completed');

END IF;

END $$;

CREATE TABLE IF NOT EXISTS "ChannelQueue" (
    channel_id int NOT NULL PRIMARY KEY,
    chahnel_status process_status NOT NULL
);