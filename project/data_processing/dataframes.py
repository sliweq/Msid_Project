import os
from dataclasses import dataclass

import pandas as pd


def create_weather_dataframe() -> pd.DataFrame:
    dataframes = []
    columns = [
        "Station Code",
        "Station Name",
        "Year",
        "Month",
        "Day",
        "Max Temp",
        "T MAX Status",
        "Min Temp",
        "T MIN Status",
        "Std Temp",
        "STD Status",
        "Ground Temp",
        "TMNG Status",
        "Precip Sum",
        "SMBD Status",
        "Precip Type",
        "Snow",
        "PKSN Status",
    ]  # based on k_d_format.txt

    # create a list of dataframes
    for file in os.listdir(os.path.join(os.getcwd(), "project/data")):
        if file.endswith(".csv"):
            dataframes.append(
                pd.read_csv(
                    os.path.join(os.getcwd(), f"project/data/{file}"),
                    encoding="unicode_escape",
                    sep=",",
                    header=None,
                    names=columns,
                )
            )

    # filter dataframes to only contain data for PSZCZYNA
    correct_station = []
    for dataframe in dataframes:
        correct_station.append(dataframe[dataframe["Station Name"] == "PSZCZYNA"])

    # remove unnecessary columns
    columns = ["Year", "Month", "Day", "Std Temp", "Precip Sum", "Precip Type"]

    correct_station = [i.loc[:, columns] for i in correct_station]
    for i in correct_station:
        i["Date"] = pd.to_datetime(i[["Year", "Month", "Day"]])
        i.drop(columns=["Year", "Month", "Day"], inplace=True)

    # change order of columns
    correct_station = [
        i[["Date", "Std Temp", "Precip Sum", "Precip Type"]] for i in correct_station
    ]

    data = pd.concat(correct_station)
    data = data.sort_values(by="Date").reset_index(drop=True)
    data["Precip Type"] = data["Precip Type"].fillna("-")
    
    return data


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
    """A class representing dataframes for police data, holidays data, and weekends."""

    police_data: pd.DataFrame = None
    holidays_data: pd.DataFrame = None
    weekends: pd.DataFrame = None
    weather: pd.DataFrame = None
    year: int = 2023

    def fix_police_data(self) -> bool:
        """Fixes the police data dataframe by selecting specific columns."""
        if self.police_data:
            columns = [
                "Data",
                "Wypadki drogowe",
                "Zabici w wypadkach",
                "Ranni w wypadkach",
            ]

            self.police_data = self.police_data.loc[:, columns]
            return True
        return False

    def fix_holidays_data(self) -> bool:
        """Fixes the holidays data dataframe by selecting specific columns,
        converting date format, and adding additional columns for month and day."""
        if self.holidays_data:
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
            self.holidays_data = self.holidays_data.loc[:, columns_list]
            self.holidays_data.columns = columns_list
            self.holidays_data = self.holidays_data.reset_index(drop=True)
            self.holidays_data["Month"] = self.holidays_data["Date"].apply(
                lambda x: polish_months[x.split()[1]]
            )
            self.holidays_data["Day"] = self.holidays_data["Date"].apply(
                lambda x: int(x.split()[0])
            )
            self.holidays_data["Date"] = pd.to_datetime(
                str(self.year)
                + "-"
                + self.holidays_data["Month"].astype(str)
                + "-"
                + self.holidays_data["Day"].astype(str)
            )
            self.holidays_data.drop(columns=["Month", "Day"], inplace=True)
            return True
        return False
