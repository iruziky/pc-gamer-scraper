class ScraperError(Exception):
    """Base exception for errors."""
    pass

class ScraperNetworkError(ScraperError):
    """Specific error for network/HTTP issues during scraping."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

class ScraperParsingError(ScraperError):
    """Specific error for issues parsing HTML or JSON."""
    pass

class ScraperDataNotFoundError(ScraperParsingError):
    """Specific error when a critical element (like the JSON script) isn't found."""
    pass