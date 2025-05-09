-- models/marts/dim_video.sql

with base as (
  select * from {{ ref('stg_youtube_video') }}
),

deduplicated as (
  select
    video_id,
    title,
    channel_id,
    published_at,
    row_number() over (partition by video_id order by retrieved_at desc) as row_num
  from base
)

select
  video_id,
  title,
  channel_id,
  published_at
from deduplicated
where row_num = 1
