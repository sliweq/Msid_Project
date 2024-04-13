import logging
from abc import ABC, abstractmethod
from datetime import datetime
from time import sleep
from typing import Optional, Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()


class Downloader(ABC):
    """Abstract class for downloading data from the web"""

    def __init__(self, url: str):
        if not url or url == "":
            raise ValueError("URL cannot be empty")
        self.url: str = url

    @abstractmethod
    def download(self):
        pass


class PoliceDataDownloader(Downloader):
    """
        Class for downloading specific data from Polish Police website
    Args:
        url : str
            URL to the website with data
    Methods:
        download() -> None
            Downloads data from the website and stores it in a pandas DataFrame
    """

    def __init__(
        self, url: str = "https://policja.pl/pol/form/1,Informacja-dzienna.html?page=0"
    ):
        super().__init__(url)
        self.recived_data: list[pd.DataFrame] = []
        self.data: pd.DataFrame = None

    def download(self, accidents_year: int = 2023):
        page_iterator = 0
        if accidents_year > datetime.now().year:
            raise ValueError("Year cannot be greater than current year!")
        tmp = self._find_first_page(accidents_year)
        print(tmp)
        if tmp is None:
            return
        print(self._find_last_page(accidents_year, tmp[0]))
        # data = self._download_data(self.url)
        # if data is None:
        #     return

        # first_year = datetime.strptime(data.loc[0,"Data"], '%Y-%m-%d').year
        # last_year = datetime.strptime(data.loc[len(data)-1,"Data"], '%Y-%m-%d').year

        # while first_year > accidents_year or last_year > accidents_year:
        #     page_iterator += 1
        #     data = self._download_data(url + f"{page_iterator}")
        #     first_year = datetime.strptime(data.loc[0,"Data"], '%Y-%m-%d').year
        #     last_year = datetime.strptime(data.loc[len(data)-1,"Data"], '%Y-%m-%d').year

        # print(data.loc[0,"Data"])
        # data = self.__download_data(self.url)
        # print(data.loc[[0]])
        # print(data.loc[[len(data)-1]])

        # self.__download_data(self.url)
        # print(self.recived_data)

    def _download_data(self, unique_url: str) -> Optional[pd.DataFrame]:
        sleep(5)
        response = requests.get(unique_url)
        if response.status_code == 200:
            logger.debug("Successfully downloaded data")
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="table-listing table-striped margin_b20")
            if table:
                return pd.read_html(str(table))[0]
            return None
        else:
            logging.error(
                f"Failed to download data, error code {response.status_code}"
                f"\nfrom url: {unique_url}"
            )

            return None

    def _find_first_page(self, accidents_year: int) -> Optional[Tuple[int, int]]:
        """_summary_

        Args:
            accidents_year (int): _description_

        Returns:
            Optional[Tuple[int, int]]: _description_
        """
        data = self._download_data(self.url)

        if data is None or len(data) == 0:
            return None

        url = self.url[:-1]

        first_year = datetime.strptime(data.loc[0, "Data"], "%Y-%m-%d").year
        last_year = datetime.strptime(data.loc[len(data) - 1, "Data"], "%Y-%m-%d").year
        page_iterator = 0
        while first_year > accidents_year or last_year > accidents_year:
            page_iterator += 1
            data = self._download_data(url + f"{page_iterator}")
            if data is None or len(data) == 0:
                return None
            first_year = datetime.strptime(data.loc[0, "Data"], "%Y-%m-%d").year
            last_year = datetime.strptime(
                data.loc[len(data) - 1, "Data"], "%Y-%m-%d"
            ).year

        for index, row in data.iterrows():

            if datetime.strptime(row["Data"], "%Y-%m-%d").year == accidents_year:
                return (page_iterator, index)
        return None

    def _find_last_page(
        self, accidents_year: int, first_page: int
    ) -> Optional[Tuple[int, int]]:
        """_summary_

        Args:
            accidents_year (int): _description_

        Returns:
            Optional[Tuple[int, int]]: _description_
        """
        url = self.url[:-1]
        data = self._download_data(url + f"{first_page}")
        if data is None or len(data) == 0:
            return None
        first_year = datetime.strptime(data.loc[0, "Data"], "%Y-%m-%d").year
        last_year = datetime.strptime(data.loc[len(data) - 1, "Data"], "%Y-%m-%d").year
        page_iterator = first_page

        while first_year >= accidents_year and last_year >= accidents_year:
            page_iterator += 1
            data = self._download_data(url + f"{page_iterator}")
            if data is None or len(data) == 0:
                return None
            first_year = datetime.strptime(data.loc[0, "Data"], "%Y-%m-%d").year
            last_year = datetime.strptime(
                data.loc[len(data) - 1, "Data"], "%Y-%m-%d"
            ).year

        for index, row in data.iterrows():

            if datetime.strptime(row["Data"], "%Y-%m-%d").year == accidents_year:
                return (page_iterator, index)
        return None
