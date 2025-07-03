import os
import logging
from datetime import datetime

def setup_logging():
    """
    Sets up logging configuration and creates log directory
    Returns the logger instance
    """
    # Creating logs directory to store log files
    LOG_DIR = "logs"
    LOG_DIR = os.path.join(os.getcwd(), LOG_DIR)
    
    # Creating LOG_DIR if it doesn't exist
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Creating filename for log file based on current timestamp
    CURRENT_TIME_STAMP = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file_name = f"log_{CURRENT_TIME_STAMP}.log"
    
    # Creating file path for log file
    log_file_path = os.path.join(LOG_DIR, file_name)
    
    # Configure logging
    logging.basicConfig(
        filename=log_file_path,
        filemode="w",
        format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        force=True  # This ensures the configuration is applied
    )
    
    # Create and return logger
    logger = logging.getLogger(__name__)
    logger.info("Logging setup completed successfully")
    
    print(f"Log file created at: {log_file_path}")
    return logger

# You can also create a global logger instance
logger = setup_logging()