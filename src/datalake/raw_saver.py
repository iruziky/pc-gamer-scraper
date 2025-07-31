import logging

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        pass
    
    @staticmethod
    def save_response_content(response_text: str, file_name: str):
        """Saves the given text content to a file."""
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(response_text)
            logger.info(f"Content successfully saved to '{file_name}'")
        except IOError as e:
            logger.error(f"Error saving file '{file_name}': {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while processing the response: {e}")