with source as (
  select * from {{ source('youtube_schema', 'youtube_video_data') }}
)

select
  video_id,
  title,
  cast(published_at as timestamp) as published_at,
  channel_id,
  cast(view_count as integer) as view_count,
  cast(like_count as integer) as like_count,
  cast(comment_count as integer) as comment_count,
  cast(retrieved_at as timestamp) as retrieved_at
from source
