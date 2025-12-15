import json
import os
import asyncio
import asyncpg
from dateutil import parser as dateparser
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")


async def load_videos(json_path):
    print(f"Loading JSON from: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    videos = data.get("videos", data)

    print(f"Found {len(videos)} videos.")

    conn = await asyncpg.connect(DATABASE_URL)

    async with conn.transaction():

        for video in videos:
            video_id = video["id"]
            creator_id = video.get("creator_id")
            video_created_at = dateparser.parse(video["video_created_at"]) if video.get("video_created_at") else None

            # Insert video row
            await conn.execute("""
                INSERT INTO videos (
                    id, creator_id, video_created_at,
                    views_count, likes_count, comments_count, reports_count,
                    created_at, updated_at
                )
                VALUES ($1,$2,$3,$4,$5,$6,$7, NOW(), NOW())
                ON CONFLICT (id) DO UPDATE SET
                    creator_id = EXCLUDED.creator_id,
                    video_created_at = EXCLUDED.video_created_at,
                    views_count = EXCLUDED.views_count,
                    likes_count = EXCLUDED.likes_count,
                    comments_count = EXCLUDED.comments_count,
                    reports_count = EXCLUDED.reports_count,
                    updated_at = NOW();
            """,
            video_id, creator_id, video_created_at,
            video.get("views_count"), video.get("likes_count"),
            video.get("comments_count"), video.get("reports_count"))

            snapshots = (
                video.get("snapshots")
                or video.get("video_snapshots")
                or video.get("hourly_snapshots")
                or []
            )

            for snap in snapshots:
                snap_id = snap["id"]
                created_at = dateparser.parse(snap["created_at"])

                await conn.execute("""
                    INSERT INTO video_snapshots (
                        id, video_id,
                        views_count, likes_count, comments_count, reports_count,
                        delta_views_count, delta_likes_count, delta_comments_count, delta_reports_count,
                        created_at, updated_at
                    )
                    VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11, NOW())
                    ON CONFLICT (id) DO UPDATE SET
                        views_count = EXCLUDED.views_count,
                        likes_count = EXCLUDED.likes_count,
                        comments_count = EXCLUDED.comments_count,
                        reports_count = EXCLUDED.reports_count,
                        delta_views_count = EXCLUDED.delta_views_count,
                        delta_likes_count = EXCLUDED.delta_likes_count,
                        delta_comments_count = EXCLUDED.delta_comments_count,
                        delta_reports_count = EXCLUDED.delta_reports_count,
                        created_at = EXCLUDED.created_at,
                        updated_at = NOW();
                """,
                snap_id, video_id,
                snap.get("views_count"), snap.get("likes_count"),
                snap.get("comments_count"), snap.get("reports_count"),
                snap.get("delta_views_count"), snap.get("delta_likes_count"),
                snap.get("delta_comments_count"), snap.get("delta_reports_count"),
                created_at)

    await conn.close()
    print("+ Finished loading all videos and snapshots.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python load_data.py data/videos.json")
        sys.exit(1)

    json_path = sys.argv[1]
    asyncio.run(load_videos(json_path))
