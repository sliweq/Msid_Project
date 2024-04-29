import logging

from data_processing.downloaders import PoliceDataDownloader 
from setup_logging import setup_logging
from data_processing.dataframes import create_weekends_dataframe

logger = logging.getLogger()


if __name__ == "__main__":
    setup_logging()
    p = PoliceDataDownloader()
    p.download()
    data = p.get_data()
    print(data["Data"])
    # print(create_weekends_dataframe(2023))
    
