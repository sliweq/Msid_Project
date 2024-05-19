import logging
from abc import ABC, abstractmethod
from datetime import datetime
from io import StringIO
from time import sleep
from typing import Optional, Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()


class Downloader(ABC):  # pylint: disable=too-few-public-methods
    """Abstract class for downloading data from the web"""

    def __init__(self, url: str) -> None:
        """
        Initializes a Downloader object.

        Args:
            url (str): The URL from which to download the data.

        Raises:
            ValueError: If the URL is empty or None.
        """
        if not url or url == "":
            raise ValueError("URL cannot be empty")
        self.url: str = url

    @abstractmethod
    def download(self) -> None:
        """
        Abstract method for downloading data.

        This method should be implemented by subclasses.
        """


class PoliceDataDownloader(Downloader):
    """
    Class for downloading specific data from Polish Police website

    Args:
        url (str): URL to the website with data

    Methods:
        download(accidents_year: int = 2023) -> None:
            Downloads data from the website and stores it in a pandas DataFrame

    Attributes:
        recived_data (list[pd.DataFrame]): List to store the received data
        data (pd.DataFrame): DataFrame to store the concatenated data
    """

    def __init__(
        self, url: str = "https://policja.pl/pol/form/1,Informacja-dzienna.html?page=0"
    ) -> None:
        super().__init__(url)
        self.recived_data: list[pd.DataFrame] = []
        self.data: pd.DataFrame = None

    def get_data(self) -> pd.DataFrame:
        """
        Returns the downloaded data

        Returns:
            pd.DataFrame: The downloaded data
        """
        return self.data.sort_values(by="Data").reset_index(drop=True)

    def _concat_data(self) -> None:
        """
        Concatenates the received data into a single DataFrame
        """
        self.data = pd.concat(self.recived_data, ignore_index=True)

    def download(self, accidents_year: int = 2023) -> None:
        """
        Downloads data from the website and stores it in a pandas DataFrame

        Args:
            accidents_year (int): The year for which to download the data

        Raises:
            ValueError: If accidents_year is greater than the current year
        """
        if accidents_year > datetime.now().year:
            raise ValueError("Year cannot be greater than current year!")

        first_page = self._find_first_page(accidents_year)

        if first_page is None:
            logger.error("Failed to find page with given year!")
            return
        last_page = self._find_last_page(accidents_year, first_page[0])
        if last_page is None:
            logger.error("Failed to find page with given year!")
            return

        if self._download_specific_pages(first_page, last_page):
            self._concat_data()
            logger.info("Data downloaded successfully!")
        else:
            logger.error("Failed to download data!")

    def _get_raw_url(self) -> str:
        url = self.url.split("=")
        if len(url) > 1:
            return "=".join(url[:-1]) + "="
        return "=".join(url[:-1]) + "="

    def _download_data(self, unique_url: str) -> Optional[pd.DataFrame]:
        sleep(0.7)
        response = requests.get(unique_url, timeout=5)  # Add timeout argument
        if response.status_code == 200:
            logger.debug("Successfully downloaded data")
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="table-listing table-striped margin_b20")
            if table:
                return pd.read_html(StringIO(str(table)))[0]
            return None
        logging.error(
            "Failed to download data, error code %s \nfrom url: %s",
            response.status_code,
            unique_url,
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

        while first_year > accidents_year and last_year > accidents_year:
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

        while first_year >= accidents_year or last_year >= accidents_year:
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

    def _download_specific_pages(
        self, first_page: Tuple[int, int], last_page: Tuple[int, int]
    ) -> bool:
        url = self._get_raw_url()
        data = self._download_data(url + f"{first_page[0]}")

        if data is None or len(data) == 0:
            self.recived_data.clear()
            return False

        self.recived_data.append(data.loc[first_page[1] :])

        for page in range(first_page[0] + 1, last_page[0]):

            data = self._download_data(url + f"{page}")
            if data is None or len(data) == 0:
                self.recived_data.clear()
                return False
            self.recived_data.append(data)

        data = self._download_data(url + f"{last_page[0]}")
        if data is None or len(data) == 0:
            self.recived_data.clear()
            return False
        self.recived_data.append(data.loc[: last_page[1]])
        return True


class HolidaysDataDownloader(Downloader):
    """
    A class for downloading holidays data from a specific URL.

    Attributes:
        url (str): The URL from which to download the data.
        data (pd.DataFrame): The downloaded data as a pandas DataFrame.
        year (Optional[int]): The year for which the data is downloaded.

    Methods:
        get_data(): Returns the downloaded data.
        get_year(): Returns the year for which the data is downloaded.
        download(year: int = 2023): Downloads the data for the specified year.
        _download_data(url: str): Downloads the data from the specified URL.
        remove_useless_data(): Removes useless data from the downloaded data.
    """

    def __init__(
        self, url: str = "https://www.timeanddate.com/holidays/poland/"
    ) -> None:
        super().__init__(url)
        self.data: pd.DataFrame = None
        self.year: Optional[int] = None

    def get_data(self) -> pd.DataFrame:
        return self.data

    def get_year(self) -> Optional[int]:
        return self.year

    def download(self, year: int = 2023) -> None:
        """
        Downloads the holidays data for the specified year.

        Args:
            year (int): The year for which to download the data. Defaults to 2023.

        Raises:
            ValueError: If the specified year is greater than the current year.

        Returns:
            None
        """
        self.year = year
        if year > datetime.now().year:
            raise ValueError("Year cannot be greater than current year!")
        data = self._download_data(self.url + f"{year}")
        if data is not None:
            self.data = data.dropna()
            self.remove_useless_data()
            logger.info("Data downloaded successfully!")
        else:
            logger.error("Failed to download data!")

    def _download_data(self, url: str) -> Optional[pd.DataFrame]:
        """
        Downloads the data from the specified URL.

        Args:
            url (str): The URL from which to download the data.

        Returns:
            Optional[pd.DataFrame]: The downloaded data as a pandas DataFrame, or None if the download failed.
        """
        sleep(0.7)
        response = requests.get(url, timeout=5)  # Add timeout argument
        if response.status_code == 200:
            logger.debug("Successfully downloaded data")
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find(
                "table",
                class_="table table--left table--inner-borders-rows table--full-width table--sticky table--holidaycountry",
            )
            if table:
                return pd.read_html(StringIO(str(table)))[0]
            return None
        logging.error(
            "Failed to download data, error code %s \nfrom url: %s",
            response.status_code,
            url,
        )
        return None

    def remove_useless_data(self) -> None:
        """
        Removes useless data from the downloaded data.

        Returns:
            None
        """
        indices_to_drop = []
        for number, row in enumerate(self.data.values):
            if "National holiday" not in row:
                indices_to_drop.append(self.data.index[number])
        self.data = self.data.drop(indices_to_drop)


class WeatherDataDownloader:
    def __init__(self, year: int = 2023) -> None:
        if year < 2001:
            raise ValueError("Year cannot be less than 2001!")
        if year > datetime.now().year:
            raise ValueError("Year cannot be greater than current year!")
        self.year = year
        self.url = f"https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/{self.year}"

    def download(self) -> None:
        for i in range(12):
            self._download(i + 1)

    def _download(self, m: int) -> None:
        if m < 10:
            response = requests.get(self.url + f"/{self.year}_0{m}_k.zip", timeout=5)
        else:
            response = requests.get(self.url + f"/{self.year}_{m}_k.zip", timeout=5)
        if response.status_code == 200:
            open(f"{self.year}_{m}_k.zip", "wb").write(response.content)
            return

        logging.error(
            "Failed to download data, error code %s \nfrom url: %s",
            response.status_code,
            self.url + f"{self.year}_{m}_k.zip",
        )
        return

def save_police_data_to_file(police_data : pd.DataFrame) -> None:
    """
    Save the police data to a CSV file in the 'project/data' directory.

    This function saves the police data to a CSV file in the 'project/data' directory.
    The file is named 'police_data.csv'.

    Args:
        police_data: DataFrame containing the police data.

    Returns:
        None
    """
    police_data.to_csv("project/data/police_data.csv", index=False)
    