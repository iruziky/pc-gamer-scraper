import logging
import sys

def setup_logging():
    """
    Configures the logging system for the entire application.

    This function sets up a root logger with a consistent format and level.
    It clears any existing handlers to prevent duplicate log output.

    Two handlers are added:
    1.  StreamHandler: Outputs log records to the console (stdout).
    2.  FileHandler: Writes log records to a file named 'app.log' in append mode.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)
    
    file_handler = logging.FileHandler("app.log", mode='a', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(file_handler)
    
    logging.info("Logging system configured.")
