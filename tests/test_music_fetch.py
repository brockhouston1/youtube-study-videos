from src.music.youtube_music_fetcher import MusicFetcher
from src.utils.logger import logger

def test_music_fetch():
    logger.info("=== 1-Hour Lofi Track Downloader ===")
    
    try:
        fetcher = MusicFetcher()
        
        while True:
            # Show available tracks
            fetcher.list_available_tracks()
            
            # Get user choice
            print("\nOptions:")
            print("1. Enter track key to download")
            print("2. Type 'all' to download all tracks")
            print("3. Type 'exit' to quit")
            
            choice = input("\nYour choice: ").strip().lower()
            
            if choice == 'exit':
                break
            elif choice == 'all':
                for track_key in fetcher.LONG_TRACKS.keys():
                    track_path = fetcher.download_long_track(track_key)
                    if track_path:
                        logger.info(f"✓ Downloaded: {track_key}")
            else:
                track_path = fetcher.download_long_track(choice)
                if track_path:
                    logger.info("✓ Track ready for use!")
            
            another = input("\nDownload another track? (y/n): ").lower()
            if another != 'y':
                break
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_music_fetch() 