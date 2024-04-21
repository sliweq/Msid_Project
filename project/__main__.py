import logging

# from data_processing.downloaders import PoliceDataDownloader 
from .setup_logging import setup_logging

logger = logging.getLogger()


if __name__ == "__main__":
    setup_logging()
