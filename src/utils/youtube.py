from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import pickle
import os

from src.utils.logger import logger
from src.config.settings import (
    CLIENT_SECRETS_FILE,
    YOUTUBE_SCOPES,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    VIDEO_TITLE_TEMPLATE,
    VIDEO_DESCRIPTION_TEMPLATE,
    VIDEO_TAGS
)

class YouTubeUploader:
    def __init__(self):
        self.credentials = None
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """Handle OAuth2 authentication with YouTube API"""
        try:
            # Check if we have stored credentials
            if os.path.exists('token.pickle'):
                logger.debug("Loading stored credentials")
                with open('token.pickle', 'rb') as token:
                    self.credentials = pickle.load(token)

            # If credentials don't exist or are invalid, get new ones
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    logger.info("Refreshing access token")
                    self.credentials.refresh(Request())
                else:
                    logger.info("Fetching new tokens")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
                    self.credentials = flow.run_local_server(port=0)

                # Save credentials for future use
                logger.debug("Saving credentials")
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.credentials, token)

            self.youtube = build(
                YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                credentials=self.credentials
            )
            logger.info("✓ YouTube API authentication successful")

        except Exception as e:
            logger.error(f"❌ Authentication failed: {str(e)}")
            raise

    def upload_video(self, video_path, title=None, description=None, tags=None):
        """Upload a video to YouTube"""
        try:
            logger.info(f"Starting upload process for: {video_path}")

            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")

            # Prepare video metadata
            date_str = datetime.now().strftime('%B %d, %Y')
            body = {
                'snippet': {
                    'title': title or VIDEO_TITLE_TEMPLATE.format(date=date_str),
                    'description': description or VIDEO_DESCRIPTION_TEMPLATE,
                    'tags': tags or VIDEO_TAGS,
                    'categoryId': '27'  # Education category
                },
                'status': {
                    'privacyStatus': 'private',  # Start as private for safety
                    'selfDeclaredMadeForKids': False,
                }
            }

            # Create upload request
            insert_request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=MediaFileUpload(
                    video_path,
                    chunksize=-1,
                    resumable=True
                )
            )

            # Upload the video
            logger.info("Uploading video...")
            response = None
            while response is None:
                status, response = insert_request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"Upload progress: {progress}%")

            logger.info(f"✓ Upload successful! Video ID: {response['id']}")
            return response['id']

        except Exception as e:
            logger.error(f"❌ Upload failed: {str(e)}")
            raise

    def update_video_privacy(self, video_id, privacy_status='public'):
        """Update the privacy status of a video"""
        try:
            self.youtube.videos().update(
                part='status',
                body={
                    'id': video_id,
                    'status': {
                        'privacyStatus': privacy_status
                    }
                }
            ).execute()
            logger.info(f"✓ Video privacy updated to {privacy_status}")
        except Exception as e:
            logger.error(f"❌ Failed to update video privacy: {str(e)}")
            raise 