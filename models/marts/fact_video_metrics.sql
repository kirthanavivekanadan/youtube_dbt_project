-- models/marts/fact_video_metrics.sql

select
  video_id,
  cast(retrieved_at as date) as metric_date,
  max(view_count) as view_count,
  max(like_count) as like_count,
  max(comment_count) as comment_count
from {{ ref('stg_youtube_video') }}
group by video_id, cast(retrieved_at as date)
