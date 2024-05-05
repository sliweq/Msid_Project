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
            "Date": pd.date_range(
                start=f"{year}-01-01", end=f"{year}-12-31", freq="W-FRI"
            )
        }
    )
    saturdays = pd.DataFrame(
        {
            "Date": pd.date_range(
                start=f"{year}-01-01", end=f"{year}-12-31", freq="W-SAT"
            )
        }
    )
    sundays = pd.DataFrame(
        {
            "Date": pd.date_range(
                start=f"{year}-01-01", end=f"{year}-12-31", freq="W-SUN"
            )
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
    year: int = 2023

    def fix_police_data(self) -> bool:
        if self.policeData:
            columns = [
                "Data",
                "Wypadki drogowe",
                "Zabici w wypadkach",
                "Ranni w wypadkach",
            ]

            self.policeData = self.policeData.loc[:, columns]
            return True
        return False

    def fix_holidays_data(self) -> bool:
        if self.holidaysData:
            polish_months = {
                "sty": 1,
                "lut": 2,
                "mar": 3,
                "kwi": 4,
                "maj": 5,
                "cze": 6,
                "lip": 7,
                "sie": 8,
                "wrz": 9,
                "paź": 10,
                "lis": 11,
                "gru": 12,
            }
            columns_list = ["Date", "Name"]
            self.holidaysData = self.holidaysData.loc[:, columns_list]
            self.holidaysData.columns = columns_list
            self.holidaysData = self.holidaysData.reset_index(drop=True)
            self.holidaysData["Month"] = self.holidaysData["Date"].apply(
                lambda x: polish_months[x.split()[1]]
            )
            self.holidaysData["Day"] = self.holidaysData["Date"].apply(
                lambda x: int(x.split()[0])
            )
            self.holidaysData["Date"] = pd.to_datetime(
                str(self.year)
                + "-"
                + self.holidaysData["Month"].astype(str)
                + "-"
                + self.holidaysData["Day"].astype(str)
            )
            self.holidaysData.drop(columns=["Month", "Day"], inplace=True)
            return True
        return False
