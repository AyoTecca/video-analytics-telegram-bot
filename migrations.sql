CREATE TABLE IF NOT EXISTS videos (
    id TEXT PRIMARY KEY,                        -- video UUID
    creator_id TEXT NOT NULL,                   -- creator identifier
    video_created_at TIMESTAMPTZ,               -- when video was published

    views_count BIGINT DEFAULT 0,
    likes_count BIGINT DEFAULT 0,
    comments_count BIGINT DEFAULT 0,
    reports_count BIGINT DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW(),       -- service fields
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_videos_creator ON videos (creator_id);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON videos (video_created_at);


CREATE TABLE IF NOT EXISTS video_snapshots (
    id TEXT PRIMARY KEY,                         -- snapshot UUID
    video_id TEXT NOT NULL REFERENCES videos(id) ON DELETE CASCADE,

    views_count BIGINT DEFAULT 0,
    likes_count BIGINT DEFAULT 0,
    comments_count BIGINT DEFAULT 0,
    reports_count BIGINT DEFAULT 0,

    delta_views_count BIGINT DEFAULT 0,
    delta_likes_count BIGINT DEFAULT 0,
    delta_comments_count BIGINT DEFAULT 0,
    delta_reports_count BIGINT DEFAULT 0,

    created_at TIMESTAMPTZ NOT NULL,             -- hourly snapshot timestamp
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_snapshots_video    ON video_snapshots (video_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_created  ON video_snapshots (created_at);
CREATE INDEX IF NOT EXISTS idx_snapshots_delta    ON video_snapshots (delta_views_count);

CREATE INDEX IF NOT EXISTS idx_snapshots_video_created 
    ON video_snapshots (video_id, created_at);
