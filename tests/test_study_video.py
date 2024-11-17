from src.pipeline.study_video_creator import StudyVideoCreator
from src.utils.logger import logger
import os
import time

def test_study_video_creation():
    logger.info("=== Testing Complete Study Video Creation ===")
    
    try:
        start_time = time.time()
        
        # Create 1-hour study video
        creator = StudyVideoCreator()
        video_path = creator.create_study_video(duration_hours=1)
        
        if video_path and os.path.exists(video_path):
            duration = time.time() - start_time
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            
            logger.info("\nResults:")
            logger.info(f"✓ Study video created successfully!")
            logger.info(f"Location: {video_path}")
            logger.info(f"Size: {size_mb:.2f} MB")
            logger.info(f"Generation time: {duration:.2f} seconds")
            logger.info(f"Duration: 1 hour")
            
            # Verify video duration using FFmpeg
            logger.info("\nVerifying video duration...")
            cmd = [
                'ffprobe', 
                '-v', 'error', 
                '-show_entries', 'format=duration', 
                '-of', 'default=noprint_wrappers=1:nokey=1', 
                str(video_path)
            ]
            
            import subprocess
            result = subprocess.run(cmd, capture_output=True, text=True)
            actual_duration = float(result.stdout.strip())
            
            logger.info(f"Verified duration: {actual_duration:.2f} seconds")
            assert abs(actual_duration - 3600) < 1, "Video duration mismatch"
            
            logger.info("\n✓ All checks passed!")
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_study_video_creation() 