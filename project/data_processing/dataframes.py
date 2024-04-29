from data_processing.downloaders import PoliceDataDownloader, HolidaysDataDownloader
from dataclasses import dataclass
import pandas as pd

def create_weekends_dataframe(year: int = 2023) -> pd.DataFrame:
    """
    Create a dataframe containing all the weekends (Friday, Saturdays and Sundays) for a given year.

    Args:
        year (int): The year for which the weekends dataframe is to be created. Defaults to 2023.

    Returns:
        pd.DataFrame: A dataframe containing the dates of all the weekends in the specified year.
    """
    weekends = pd.DataFrame(
        {
            "Date": pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="W-FRI")
        }
    )
    saturdays = pd.DataFrame(
        {
            "Date": pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="W-SAT")
        }
    )
    sundays = pd.DataFrame(
        {
            "Date": pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="W-SUN")
        }
    )
    weekends = pd.concat([weekends, saturdays, sundays]).reset_index(drop=True)
    weekends["Date"] = weekends["Date"].dt.strftime("%Y-%m-%d")
    weekends = weekends.sort_values(by="Date").reset_index(drop=True)
    return weekends



@dataclass
class Data: 
    policeData: pd.DataFrame
    holidaysData: pd.DataFrame
    weekends: pd.DataFrame
    
    def fix_police_data(self, columns: list[str]) -> None:
        for column in columns:
            if column in self.policeData.columns:
                self.policeData[column] = self.policeData.drop(column, axis=1)
        
    def fix_holidays_data(self, columns: list[str]) -> None:
        for column in columns:
            if column in self.holidaysData.columns:
                self.holidaysData[column] = self.holidaysData.drop(column, axis=1)
    