import logging

from data_processing.dataframes import (  # type: ignore # pylint: disable=import-error
    Data, create_weather_dataframe)
from data_processing.downloaders import (  # type: ignore # pylint: disable=import-error
    PoliceDataDownloader, WeatherDataDownloader)
from data_processing.move_data import (delete_useless_files, move_zip_files,
                                       unzip_files)
from setup_logging import \
    setup_logging  # type: ignore # pylint: disable=import-error

logger = logging.getLogger()

if __name__ == "__main__":
    setup_logging()
    # p = PoliceDataDownloader()
    # p.download(2024)

    # w = WeatherDataDownloader(2022)
    # w.download()
    # move_zip_files()
    # unzip_files()
    # delete_useless_files()

    create_weather_dataframe()

    # data = p.get_data()
    # for i,n in data.iterrows():
    #     print(i)
    #     print(n["Data"])

    # print(create_weekends_dataframe(2023))

    # d = Data(policeData=p.get_data(), holidaysData=None, weekends=None, year=2024)

    # d.fix_police_data()
    # print(d.policeData)
