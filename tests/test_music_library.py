from src.music.music_library import MusicLibrary
from src.utils.logger import logger

def test_music_library():
    logger.info("=== Testing Music Library: Adding CC0 Lofi Tracks ===")
    
    try:
        library = MusicLibrary()
        
        # CC0 Licensed Tracks (No Attribution Required)
        tracks_to_add = [
            # 30-minute tracks
            {
                'url': 'https://pixabay.com/music/beats-lofi-study-112191/',
                'title': 'Lofi Study',
                'artist': 'FASSounds',
                'license_type': 'CC0',
                'duration': 1800,  # 30 minutes
                'bpm': 80,
                'mood': 'focused'
            },
            {
                'url': 'https://pixabay.com/music/ambient-chill-lofi-108566/',
                'title': 'Ambient Chill',
                'artist': 'SoulProdMusic',
                'license_type': 'CC0',
                'duration': 1800,
                'bpm': 75,
                'mood': 'relaxed'
            },
            
            # 1-hour tracks
            {
                'url': 'https://pixabay.com/music/beats-lofi-chill-114954/',
                'title': 'Lofi Chill Hour',
                'artist': 'Music_Unlimited',
                'license_type': 'CC0',
                'duration': 3600,
                'bpm': 85,
                'mood': 'chill'
            },
            
            # Short loops (5-10 minutes)
            {
                'url': 'https://pixabay.com/music/beats-lofi-hip-hop-118973/',
                'title': 'Lofi Loop',
                'artist': 'BeepCode',
                'license_type': 'CC0',
                'duration': 300,  # 5 minutes
                'bpm': 90,
                'mood': 'upbeat'
            }
        ]
        
        # Ambient Cafe Sounds (to mix with lofi)
        ambient_tracks = [
            {
                'url': 'https://pixabay.com/sound-effects/coffee-shop-ambience-8797/',
                'title': 'Cafe Ambience',
                'artist': 'SoundGallery',
                'license_type': 'CC0',
                'duration': 180,  # 3 minutes loop
                'bpm': None,
                'mood': 'ambient'
            }
        ]
        
        logger.info("\nAdding tracks to library...")
        
        for track_info in tracks_to_add:
            library.add_track(**track_info)
            
        for track_info in ambient_tracks:
            library.add_track(**track_info)
            
        logger.info(f"✓ Added {len(tracks_to_add) + len(ambient_tracks)} tracks to library")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_music_library() 