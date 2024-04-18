DROP TABLE IF EXISTS "prediction";

CREATE TABLE IF NOT EXISTS prediction (
    id uuid NOT NULL,
    video_id uuid NOT NULL,
    image_path text NOT NULL,
    model_name text NOT NULL,
    confidence numeric NOT NULL,
    iou numeric NOT NULL,
    detection_list text[] NOT NULL,
    created_at timestamp with time zone NOT NULL,
    CONSTRAINT prediction_pkey PRIMARY KEY (id),
    CONSTRAINT fk_video_id FOREIGN KEY (video_id) REFERENCES video (id)
);

CREATE INDEX idx_prediction_video_id ON prediction (video_id);