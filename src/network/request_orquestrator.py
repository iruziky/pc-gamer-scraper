import logging
from curl_cffi import requests

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10

class RequestOrchestrator:
    def __init__(self):
        pass

    def make_request(self, url: str) -> requests.Response | None:
        """
        Performs a web request and returns the response object if successful, else None.
        Handles request-specific errors like timeouts.
        """
        logger.info(f"Starting request to URL: {url}")
        try:
            response = requests.get(
                url,
                timeout=REQUEST_TIMEOUT,
                impersonate="chrome"
            )
            
            if response.ok:
                logger.info(f"Request to {url} successful (status 200).")
                return response
            else:
                logger.info(f"Request to {url} failed with status code {response.status_code}.")
                return None
        except requests.exceptions.Timeout as e:
            logger.error(f"Request to {url} timed out: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during the request to {url}: {e}")
            return None
        finally:
            logger.info(f"Request attempt for {url} finalized by Orchestrator.")