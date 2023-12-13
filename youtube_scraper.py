import os
from googleapiclient.discovery import build
import json
import os
from dotenv import load_dotenv

# Set your API key
api_key =os.getenv('YOUTUBE_API_KEY')

# Set the YouTube API service
youtube = build("youtube", "v3", developerKey=api_key)

def get_channel_id(channel_name):
    """
    Get the channel ID based on the channel name.
    """
    request = youtube.search().list(
        part="snippet",
        q=channel_name,
        type="channel"
    )
    response = request.execute()
    if response['items']:
        return response['items'][0]['snippet']['channelId']
    else:
        return None

def get_latest_shorts_details(channel_name, max_results=10):
    """
    Get details of the latest YouTube Shorts for a given channel name.
    """
    channel_id = get_channel_id(channel_name)
    if channel_id:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            q="shorts",
            type="video",
            maxResults=max_results,
            order="date"
        )
        response = request.execute()
        return response.get('items', [])
    else:
        return []

def get_shorts_statistics(channel_name):
    shorts_details = get_latest_shorts_details(channel_name, max_results=10)

    total_views = 0
    total_likes = 0
    total_dislikes = 0 

    for short in shorts_details:
        video_title = short['snippet']['title']
        video_id = short['id']['videoId']

        # Get video statistics
        stats_request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        stats_response = stats_request.execute()
        statistics = stats_response['items'][0]['statistics']

        views = statistics.get('viewCount', 0)
        likes = statistics.get('likeCount', 0)
        dislikes = statistics.get('dislikeCount', 0)
        
        total_views += int(views)
        total_likes += int(likes)
        total_dislikes += int(dislikes)
    return {
        'Channel Name': channel_name,
        'Average Views': total_views/10,
        'Total Likes': total_likes,
        'Total Dislikes': total_dislikes
        }

# if __name__ == "__main__":
#     main("A2D Channel")