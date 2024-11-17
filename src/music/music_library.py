from pathlib import Path
from typing import List, Optional
import json
import requests
import os
from dataclasses import dataclass
from src.utils.logger import logger
from src.config.settings import MUSIC_DIR

@dataclass
class Track:
    title: str
    artist: str
    duration: int  # in seconds
    file_path: Path
    license_type: str
    bpm: Optional[int] = None
    mood: Optional[str] = None

class MusicLibrary:
    def __init__(self):
        self.library_path = MUSIC_DIR
        self.tracks: List[Track] = []
        self.metadata_file = self.library_path / "metadata.json"
        self._load_library()
    
    def _load_library(self):
        """Load existing tracks from the music directory"""
        try:
            # Create music directory if it doesn't exist
            self.library_path.mkdir(parents=True, exist_ok=True)
            
            # Load metadata if it exists
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                for track_data in metadata['tracks']:
                    track = Track(
                        title=track_data['title'],
                        artist=track_data['artist'],
                        duration=track_data['duration'],
                        file_path=self.library_path / track_data['filename'],
                        license_type=track_data['license_type'],
                        bpm=track_data.get('bpm'),
                        mood=track_data.get('mood')
                    )
                    if track.file_path.exists():
                        self.tracks.append(track)
            
            logger.info(f"Loaded {len(self.tracks)} tracks from music library")
            
        except Exception as e:
            logger.error(f"Failed to load music library: {str(e)}")
            raise

    def add_track(self, 
                 url: str, 
                 title: str, 
                 artist: str, 
                 license_type: str,
                 bpm: Optional[int] = None,
                 mood: Optional[str] = None) -> Track:
        """Add a new track to the library"""
        try:
            # Download the track
            filename = f"{title.lower().replace(' ', '_')}.mp3"
            file_path = self.library_path / filename
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Get duration using ffprobe
            duration = self._get_track_duration(file_path)
            
            # Create track object
            track = Track(
                title=title,
                artist=artist,
                duration=duration,
                file_path=file_path,
                license_type=license_type,
                bpm=bpm,
                mood=mood
            )
            
            self.tracks.append(track)
            self._save_metadata()
            
            logger.info(f"Added track: {title} by {artist}")
            return track
            
        except Exception as e:
            logger.error(f"Failed to add track: {str(e)}")
            raise

    def get_track_by_mood(self, mood: str) -> Optional[Track]:
        """Get a track matching the specified mood"""
        matching_tracks = [t for t in self.tracks if t.mood == mood]
        return matching_tracks[0] if matching_tracks else None

    def get_track_by_bpm(self, target_bpm: int, tolerance: int = 5) -> Optional[Track]:
        """Get a track matching the specified BPM (within tolerance)"""
        matching_tracks = [
            t for t in self.tracks 
            if t.bpm and abs(t.bpm - target_bpm) <= tolerance
        ]
        return matching_tracks[0] if matching_tracks else None

    def _get_track_duration(self, file_path: Path) -> int:
        """Get track duration using ffprobe"""
        import subprocess
        
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(file_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return int(float(result.stdout.strip()))

    def _save_metadata(self):
        """Save library metadata to JSON"""
        metadata = {
            'tracks': [
                {
                    'title': track.title,
                    'artist': track.artist,
                    'duration': track.duration,
                    'filename': track.file_path.name,
                    'license_type': track.license_type,
                    'bpm': track.bpm,
                    'mood': track.mood
                }
                for track in self.tracks
            ]
        }
        
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2) 