import webbrowser
from googleapiclient.discovery import build
from settings import API_KEY

MAX_DURATION = 1200
MIN_VIEW_COUNT = 100000


def get_video(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    response = youtube.videos().list(
        part='contentDetails,statistics',
        id=video_id
    ).execute()
    return response

def get_video_duration(video):
    duration = video['items'][0]['contentDetails']['duration']
    duration = duration.replace('PT', '').replace('S', '').replace('M', ':').replace('H', ':')
    duration_parts = duration.split(':')
    duration_seconds = 0
    for i in range(len(duration_parts)):
        duration_seconds += int(duration_parts[i]) * (60 ** (len(duration_parts) - i - 1))
    return duration_seconds

def get_video_view_count(video):
    return int(video["items"][0]["statistics"]["viewCount"])


youtube = build('youtube', 'v3', developerKey=API_KEY)


response = youtube.search().list(
    q='large,language,model,trained,google',
    part='id,snippet',
    maxResults=10
).execute()


video_ids = [item['id']['videoId'] for item in response['items'] if item['id']['kind'] == 'youtube#video']

video_urls = []
for video_id in video_ids:
    video  = get_video(video_id, API_KEY)
    duration_seconds = get_video_duration(video)
    view_count = get_video_view_count(video)

    if duration_seconds <= MAX_DURATION and view_count >= MIN_VIEW_COUNT:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_urls.append(video_url)
print("video count:", len(video_urls))

for url in video_urls:
     webbrowser.open(url)