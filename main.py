import argparse
import logging
import mimetypes

from src.core.logging_setup import setup_logging 
from src.datalake.raw_saver import DataLoader
from src.network.request_orquestrator import RequestOrchestrator

from datetime import datetime

logger = logging.getLogger(__name__)

def parse_arguments():
    """
    Parses command-line arguments for the script.

    Sets up an argument parser to accept a single positional argument: 'url'.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Process a web request.")
    parser.add_argument(
        "url",
        type=str,
        help="The URL to request."
    )
    return parser.parse_args()

def generate_response_filename(response):
    """
    Generate the file name for the response based in the
    current date/time and in Content-Type extension of the response.
    """
    content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
    extension = mimetypes.guess_extension(content_type)
    return f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}{extension if extension else ".html"}'

def main():
    """
    The main execution function for the scraper.

    This function orchestrates the entire process:
    1. Parses the URL from command-line arguments.
    2. Uses the RequestOrchestrator to fetch the URL's content.
    3. If successful, generates a unique filename for the response.
    4. Saves the raw response content to a local file using the DataLoader.
    """
    args = parse_arguments()
    request_orchestrator = RequestOrchestrator()
    
    response = request_orchestrator.make_request(args.url)
    if response is None:
        logger.error(f"Erro: Não foi possível obter resposta para a URL: {args.url}")
        return
    
    output_filename = generate_response_filename(response)
    DataLoader.save_response_content(response.text, output_filename)

if __name__ == "__main__":
    setup_logging()
    main()