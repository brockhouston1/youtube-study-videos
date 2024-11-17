from pathlib import Path
import shutil
from typing import Dict, List
import json

from src.utils.logger import logger
from src.config.settings import MUSIC_DIR, ASSETS_DIR

class MusicDownloader:
    def __init__(self):
        self.music_dir = MUSIC_DIR
        self.metadata_path = self.music_dir / "metadata.json"
        self.source_dir = ASSETS_DIR / "base_tracks"
        
    def setup_initial_library(self):
        """Setup initial music library from base tracks"""
        try:
            logger.info("=== Setting up Music Library ===")
            
            # Create directories if they don't exist
            self.music_dir.mkdir(parents=True, exist_ok=True)
            self.source_dir.mkdir(parents=True, exist_ok=True)
            
            # Track information
            tracks_info = {
                'lofi_base.mp3': {
                    'title': 'Lofi Study Base',
                    'artist': 'Study Music',
                    'license_type': 'CC0',
                    'duration': 180,
                    'bpm': 80,
                    'mood': 'focused'
                },
                'cafe_ambience.mp3': {
                    'title': 'Cafe Background',
                    'artist': 'Ambient Sounds',
                    'license_type': 'CC0',
                    'duration': 120,
                    'bpm': None,
                    'mood': 'ambient'
                }
            }
            
            logger.info("\nPlease add the following base tracks to:")
            logger.info(f"{self.source_dir}")
            for filename in tracks_info.keys():
                logger.info(f"- {filename}")
            
            # Check for base tracks
            missing_tracks = []
            for filename in tracks_info.keys():
                source_path = self.source_dir / filename
                if not source_path.exists():
                    missing_tracks.append(filename)
            
            if missing_tracks:
                logger.error("\nMissing base tracks:")
                for track in missing_tracks:
                    logger.error(f"- {track}")
                raise FileNotFoundError("Please add the required base tracks to continue")
            
            # Copy tracks to music directory
            successful_copies = []
            for filename, track_info in tracks_info.items():
                try:
                    source_path = self.source_dir / filename
                    dest_path = self.music_dir / filename
                    
                    logger.info(f"\nCopying: {track_info['title']}")
                    shutil.copy2(source_path, dest_path)
                    
                    if dest_path.exists():
                        track_info['file_path'] = str(dest_path)
                        successful_copies.append(track_info)
                        logger.info(f"✓ Copied: {filename}")
                    
                except Exception as e:
                    logger.error(f"Failed to copy {filename}: {str(e)}")
                    continue
            
            # Save metadata
            metadata = {
                'tracks': successful_copies
            }
            
            with open(self.metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"\n=== Music Library Setup Complete ===")
            logger.info(f"Location: {self.music_dir}")
            logger.info(f"Tracks copied: {len(successful_copies)}")
            logger.info(f"Metadata saved to: {self.metadata_path}")
            
        except Exception as e:
            logger.error(f"Failed to setup music library: {str(e)}")
            raise

def setup_music_library():
    """Convenience function to setup the music library"""
    downloader = MusicDownloader()
    downloader.setup_initial_library()

if __name__ == "__main__":
    setup_music_library()