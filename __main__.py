import logging

from data_processing.dataframes import *  # type: ignore # pylint: disable=import-error
from data_processing.downloaders import *  # type: ignore # pylint: disable=import-error
from data_processing.models import *  # type: ignore # pylint: disable=import-error
from data_processing.move_data import *  # type: ignore # pylint: disable=import-error
from data_processing.save_data import *
from setup_logging import \
    setup_logging  # type: ignore # pylint: disable=import-error
from visualization.tmp import *  # type: ignore # pylint: disable=import-error

logger = logging.getLogger()

if __name__ == "__main__":

    download_data(2022, 2023)
