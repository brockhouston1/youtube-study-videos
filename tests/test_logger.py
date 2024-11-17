from src.utils.logger import logger

def test_logger():
    logger.info("=== Testing Logger ===")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

if __name__ == "__main__":
    test_logger() 