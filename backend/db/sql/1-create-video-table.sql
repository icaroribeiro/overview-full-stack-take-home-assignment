DROP TABLE IF EXISTS "video";

CREATE TABLE IF NOT EXISTS video (
    id uuid NOT NULL,
    name text NOT NULL,
    image_path_list text[],
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT video_pkey PRIMARY KEY (id),
    CONSTRAINT video_name_key UNIQUE (name)
);

CREATE INDEX idx_video_name ON video (name);