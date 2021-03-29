import re

from googleapiclient.discovery import build
from datetime import timedelta

#Google Api key
api_key = ''

youtube = build('youtube', 'v3', developerKey = api_key)

#Regular Expressions
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

nextPageToken = None
totalSeconds = 0
while True:
    pl_request = youtube.playlistItems().list(
            part = 'contentDetails',
            playlistId = 'PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS',
            maxResults = 50,
            pageToken = nextPageToken
        )

    pl_response = pl_request.execute()

    vid_IDs = []
    for item in pl_response['items']:
        vid_ID = item['contentDetails']['videoId']
        vid_IDs.append(vid_ID)

    vid_request = youtube.videos().list(
        part = 'contentDetails',
        id = ','.join(vid_IDs)
    )

    vid_response = vid_request.execute()

    for item in vid_response['items']:
        duration = item['contentDetails']['duration']
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        video_seconds = timedelta(
            hours = hours,
            minutes = minutes,
            seconds = seconds
        ).total_seconds()
        totalSeconds += video_seconds

    nextPageToken = pl_response.get('nextPageToken')
    
    if not nextPageToken:
        break

totalSeconds = int(totalSeconds)

minutes, seconds = divmod(totalSeconds, 60)
hours, minutes = divmod(minutes, 60)

print(f'{hours}:{minutes}:{seconds}')





