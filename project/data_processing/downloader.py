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

    def concat_data(self) -> None:
        self.data = pd.concat(self.recived_data, ignore_index=True)
            

        
                
    def download(self, accidents_year: int = 2023):
        if accidents_year > datetime.now().year:
            raise ValueError("Year cannot be greater than current year!")
        
        first_page = self._find_first_page(accidents_year)
        
        if first_page is None:
            logger.error("Failed to find page with giveen year!")
            return
        last_page = self._find_last_page(accidents_year, first_page[0])
        if last_page is None:
            logger.error("Failed to find page with giveen year!")
            return
        
        if self._download_specific_pages(first_page, last_page):
            self.concat_data()
            print(self.data)
        
    def _get_raw_url(self) -> str:
        url = self.url.split("=")
        if len(url) > 1 :
            return "=".join(url[:-1]) + "="
        return "=".join(url[:-1]) + "="
        
    def _download_data(self, unique_url: str) -> Optional[pd.DataFrame]:
        sleep(0.7)
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
        url = self._get_raw_url()
        data = self._download_data(url + "0")

        if data is None or len(data) == 0:
            return None

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
        url = self._get_raw_url()
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
            
        if first_year < accidents_year or last_year < accidents_year:
            page_iterator -= 1
        data = self._download_data(url + f"{page_iterator}")
        if data is None or len(data) == 0:
            return None
        for index, row in data.iloc[::-1].iterrows():
            if datetime.strptime(row["Data"], "%Y-%m-%d").year == accidents_year:
                return (page_iterator, index)
        return None

    def _download_specific_pages(self, first_page: Tuple[int,int], last_page: Tuple[int,int]) -> bool:
        url = self._get_raw_url()
        data = self._download_data(url + f"{first_page[0]}")

        if data is None or len(data) == 0:
            self.recived_data.clear()
            return False

        self.recived_data.append(data.loc[first_page[1]:])
        
        for page in range(first_page[0]+1, last_page[0]):
            
            data = self._download_data(url + f"{page}")
            if data is None or len(data) == 0:
                self.recived_data.clear()
                return False
            self.recived_data.append(data)
        
        data = self._download_data(url + f"{last_page[0]}")
        if data is None or len(data) == 0:
            self.recived_data.clear()
            return False
        self.recived_data.append(data.loc[:last_page[1]])
        return True