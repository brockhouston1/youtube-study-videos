import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime

# Define the scope for YouTube upload
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate_youtube():
    """Authenticate and return the YouTube service."""
    creds = None
    # Check if token.json exists to load existing credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no valid credentials, prompt user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)

def generate_title():
    """Generate a dynamic title for the video."""
    date_str = datetime.now().strftime("%B %d, %Y")
    return f"Relaxing Study Session - {date_str}"

def generate_description():
    """Generate a dynamic description for the video."""
    return (
        "Enjoy this relaxing study session with calming lofi beats. "
        "Perfect for studying, working, or just unwinding. "
        "Don't forget to like and subscribe for more content!"
    )

def upload_video(youtube, video_file):
    """Upload a video to YouTube."""
    title = generate_title()
    description = generate_description()
    tags = ['study', 'lofi', 'relaxing', 'music']

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print("Upload Complete!")
    return response

if __name__ == "__main__":
    youtube_service = authenticate_youtube()
    upload_video(
        youtube_service,
        video_file='output/final_videos/final_study_video.mp4'  # Ensure this path is correct
    ) 