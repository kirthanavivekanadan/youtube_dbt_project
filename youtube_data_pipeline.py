from googleapiclient.discovery import build
import pandas as pd
import snowflake.connector
from datetime import datetime
import os

# Fetch environment variables (for AWS CodeBuild or local testing)
API_KEY = os.getenv('YOUTUBE_API_KEY', 'AIzaSyB-_2f6LvU1MqG_x90j6yDLBbPTihkpX4s')  # Replace with your actual API key
CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID', 'UCh9nVJoWXmFb7sLApWGcLPQ')

# Snowflake connection details from environment variables
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER', 'USERNAME')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD', 'password',)
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT', 'hsizyrc-')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE', 'youtube_db')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA', 'youtube_schema')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE', 'youtube_wh')
SNOWFLAKE_TABLE = os.getenv('SNOWFLAKE_TABLE', 'youtube_video_data_rev')

# Initialize the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_ids(channel_id, max_results=50):
    """Fetches the latest video IDs from the specified channel."""
    response = youtube.search().list(
        channelId=channel_id,
        part='id',
        order='date',
        maxResults=max_results
    ).execute()
    return [item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video']

def get_video_stats(video_ids):
    """Fetches video statistics and details from YouTube."""
    video_data = []
    for i in range(0, len(video_ids), 50):  # API allows a maximum of 50 at a time
        response = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i+50])
        ).execute()

        for video in response['items']:
            stats = video['statistics']
            snippet = video['snippet']
            video_data.append({
                'video_id': video['id'],
                'title': snippet['title'],
                'published_at': snippet['publishedAt'],
                'channel_id': snippet['channelId'],
                'view_count': int(stats.get('viewCount', 0)),
                'like_count': int(stats.get('likeCount', 0)),
                'comment_count': int(stats.get('commentCount', 0)),
                'retrieved_at': datetime.utcnow().isoformat()
            })
    return pd.DataFrame(video_data)

def load_to_snowflake(df):
    """Loads the fetched video data to Snowflake."""
    try:
        # Establishing Snowflake connection
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        cursor = conn.cursor()

        # Optional: Truncate the table before loading
        cursor.execute(f"TRUNCATE TABLE IF EXISTS {SNOWFLAKE_TABLE}")

        # Insert rows using bulk insert
        for _, row in df.iterrows():
            cursor.execute(f"""
                INSERT INTO {SNOWFLAKE_TABLE} (
                    video_id, title, published_at, channel_id,
                    view_count, like_count, comment_count, retrieved_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['video_id'], row['title'], row['published_at'], row['channel_id'],
                int(row['view_count']), int(row['like_count']), int(row['comment_count']), row['retrieved_at']
            ))

        conn.commit()
        print("Data loaded to Snowflake successfully.")
    except Exception as e:
        print("Error while loading data to Snowflake:", str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Fetch YouTube data
    video_ids = get_video_ids(CHANNEL_ID)
    df = get_video_stats(video_ids)

    # Load to Snowflake
    if not df.empty:
        load_to_snowflake(df)
    else:
        print("No video data found to load.")
