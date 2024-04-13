import logging

from data_processing.downloader import PoliceDataDownloader
from setup_logging import setup_logging

logger = logging.getLogger()


if __name__ == "__main__":
    setup_logging()
    PoliceDataDownloader(
        "https://policja.pl/pol/form/1,Informacja-dzienna.html?page=2"
    ).download()
