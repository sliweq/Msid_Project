import logging

from data_processing.dataframes import \
    Data  # type: ignore # pylint: disable=import-error
from data_processing.downloaders import \
    PoliceDataDownloader  # type: ignore # pylint: disable=import-error
from setup_logging import \
    setup_logging  # type: ignore # pylint: disable=import-error

logger = logging.getLogger()


if __name__ == "__main__":
    setup_logging()
    p = PoliceDataDownloader()
    p.download(2024)
    # data = p.get_data()
    # for i,n in data.iterrows():
    #     print(i)
    #     print(n["Data"])

    # print(create_weekends_dataframe(2023))

    d = Data(policeData=p.get_data(), holidaysData=None, weekends=None, year=2024)

    d.fix_police_data()
    print(d.policeData)
