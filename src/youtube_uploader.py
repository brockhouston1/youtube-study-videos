import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import pickle
from google.auth.exceptions import RefreshError

# Define the scope for YouTube upload
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate_youtube():
    """Authenticate and return the YouTube service."""
    creds = None
    token_path = 'token.pickle'
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                print("Token has been expired or revoked. Deleting token and re-authenticating.")
                os.remove(token_path)
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/brockhouston/personalProj/youtube/youtube-study-videos/client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0, access_type='offline')
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
    
    youtube_service = build('youtube', 'v3', credentials=creds)
    return youtube_service

def generate_title():
    """Generate an optimized title for the video."""
    date_str = datetime.now().strftime("%B %d, %Y")
    return f"集中 (しゅうちゅう) - Lofi Beats for Focus & Relaxation - ADHD & Anxiety Relief {date_str}"

def generate_description():
    """Generate an optimized description for the video."""
    return (
        "Experience the perfect blend of lofi beats crafted specifically for focus, productivity, and anxiety relief. "
        "Whether you're studying, working, or need help managing ADHD symptoms, this carefully curated mix creates "
        "the ideal audio environment for deep concentration and mental clarity.\n\n"

        " About This Mix:\n"
        "This unique lofi compilation features carefully selected instrumental beats, ambient sounds, and calming "
        "melodies designed to help you maintain focus while reducing stress and anxiety. Our music is specifically "
        "engineered to promote alpha brain waves, enhancing your concentration and productivity.\n\n"

        "⭐ Benefits:\n"
        "• Enhanced focus and concentration\n"
        "• Reduced anxiety and stress\n"
        "• Improved study sessions\n"
        "• Better work productivity\n"
        "• Natural ADHD management\n\n"

        "🎧 Best Used For:\n"
        "• Study sessions and exam preparation\n"
        "• Work focus and deep work periods\n"
        "• Reading and writing\n"
        "• Meditation and mindfulness\n"
        "• Background music for productivity\n\n"


        "🌟 Join Our Study Community:\n"
        "Subscribe: https://www.youtube.com/@cozycornerfocus\n"
        "lofi study music, focus music, adhd music, anxiety relief, concentration music, "
        "study beats, productivity music, background study music, calm music, focus beats, study with me, "
        "lofi hip hop, study music for concentration, adhd focus music, anxiety calming music\n\n"

        "#studymusic #lofi #focusmusic #studybeats #adhdsupport #anxietyrelief #studywithme "
        "#productivitymusic #concentrationmusic #studymotivation #lofibeats #studyplaylist #focusplaylist"
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
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False  # Set to False to indicate the video is not made for kids
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