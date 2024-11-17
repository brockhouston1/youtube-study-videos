from pathlib import Path
import yt_dlp
from typing import Optional, Dict
from src.utils.logger import logger
from src.config.settings import MUSIC_DIR

class MusicFetcher:
    def __init__(self):
        self.music_dir = MUSIC_DIR
        self.music_dir.mkdir(parents=True, exist_ok=True)
        
        # Verified working lofi tracks and streams
        self.LONG_TRACKS = {
            'study_session_1': {
                'url': 'https://www.youtube.com/watch?v=lTRiuFIWV54',
                'title': '1 Hour Study Session',
                'duration': '1 hour',
                'mood': 'focused study',
                'type': 'static video'
            },
            'lofi_girl_beats': {
                'url': 'https://www.youtube.com/watch?v=jfKfPfyJRdk',
                'title': 'Lofi Girl - Beats to Study To',
                'duration': '24/7 stream',
                'mood': 'study focus',
                'type': 'live stream'
            },
            'coffee_shop_live': {
                'url': 'https://www.youtube.com/watch?v=MYPVQccHhAQ',
                'title': 'Coffee Shop Radio',
                'duration': '24/7 stream',
                'mood': 'cafe ambience',
                'type': 'live stream'
            },
            'chill_gaming': {
                'url': 'https://www.youtube.com/watch?v=7NOSDKb0HlU',
                'title': '1 Hour Gaming Lofi',
                'duration': '1 hour',
                'mood': 'relaxed gaming',
                'type': 'static video'
            },
            'study_beats': {
                'url': 'https://www.youtube.com/watch?v=PAvDi3YKVDU',
                'title': '1 Hour Study Beats',
                'duration': '1 hour',
                'mood': 'deep focus',
                'type': 'static video'
            },
            'cozy_winter': {
                'url': 'https://www.youtube.com/watch?v=9Tcy_V8jjf8',
                'title': 'Cozy Winter Coffee Shop',
                'duration': '3 hours',
                'mood': 'winter cozy',
                'type': 'static video'
            }
        }
    
    def download_long_track(self, track_key: str) -> Optional[Path]:
        """Download a specific track or capture from stream"""
        if track_key not in self.LONG_TRACKS:
            logger.error(f"Unknown track key. Available tracks:")
            self.list_available_tracks()
            return None
            
        track_info = self.LONG_TRACKS[track_key]
        filename = f"{track_key}.mp3"
        
        try:
            output_path = self.music_dir / filename
            
            logger.info(f"\nDownloading: {track_info['title']}")
            logger.info(f"Type: {track_info['type']}")
            logger.info(f"Duration: {track_info['duration']}")
            logger.info(f"Mood: {track_info['mood']}")
            
            if track_info['type'] == 'live stream':
                logger.info("\n⚠️  This is a live stream - capturing 1 hour segment...")
                # Add stream-specific options
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': str(output_path).replace('.mp3', ''),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'quiet': False,
                    # Limit duration for streams
                    'download_ranges': lambda info: [[0, 3600]],  # 1 hour in seconds
                }
            else:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': str(output_path).replace('.mp3', ''),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'quiet': False
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([track_info['url']])
            
            if output_path.exists():
                size_mb = output_path.stat().st_size / (1024 * 1024)
                logger.info(f"\n✓ Download successful!")
                logger.info(f"Track: {track_info['title']}")
                logger.info(f"Size: {size_mb:.2f} MB")
                logger.info(f"Location: {output_path}")
                return output_path
            else:
                logger.error(f"File not found at: {output_path}")
                return None
            
        except Exception as e:
            logger.error(f"Failed to download track: {str(e)}")
            return None

    def list_available_tracks(self):
        """List all available tracks with clear stream/video distinction"""
        logger.info("\nAvailable Lofi Tracks and Streams:")
        
        # First list static videos
        logger.info("\n📼 Static Videos:")
        for key, info in self.LONG_TRACKS.items():
            if info['type'] == 'static video':
                logger.info(f"- {key}: {info['title']}")
                logger.info(f"  Duration: {info['duration']}")
                logger.info(f"  Mood: {info['mood']}")
        
        # Then list live streams
        logger.info("\n🔴 Live Streams (will capture 1 hour):")
        for key, info in self.LONG_TRACKS.items():
            if info['type'] == 'live stream':
                logger.info(f"- {key}: {info['title']}")
                logger.info(f"  Type: {info['duration']}")
                logger.info(f"  Mood: {info['mood']}")

if __name__ == "__main__":
    fetcher = MusicFetcher()
    fetcher.list_available_tracks() 