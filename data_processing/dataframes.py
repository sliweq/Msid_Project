import os
from dataclasses import dataclass

import pandas as pd


def read_csv_file(file_name: str) -> pd.DataFrame:
    """
    Read the data from the 'data' directory.

    This function reads the data from the 'data' directory.

    Returns:
        pd.DataFrame: DataFrame containing the data.
    """

    df = pd.read_csv(
        os.path.join("data", file_name), encoding="unicode_escape", sep=","
    )
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"])
    else:
        df["Date"] = pd.to_datetime(df["Date"])
    if file_name.endswith("police_data.csv"):
        df.fillna(df.mean(), inplace=True)    
    return df


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
    for file in os.listdir(os.path.join(os.getcwd(), "project", "data")):
        if file.endswith(".csv") and "k_d_" in file:
            dataframes.append(
                pd.read_csv(
                    os.path.join(os.getcwd(), "project", "data", file),
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


def create_weekends_dataframe(start_year: int, end_year: int) -> pd.DataFrame:
    """
    Create a dataframe containing all the weekends (Friday, Saturdays and Sundays) for a given year.

    Args:
        year (int): The year for which the weekends dataframe is to be created. Defaults to 2023.

    Returns:
        pd.DataFrame: A dataframe containing the dates of all the weekends in the specified year.
    """
    data = []
    for year in range(start_year, end_year + 1):
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
        data.append(weekends)

    return pd.concat(data, ignore_index=True)


def fix_police_data(police_data: pd.DataFrame) -> pd.DataFrame:
    """Fixes the police data dataframe by selecting specific columns."""

    columns = [
        "Data",
        "Wypadki drogowe",
        "Zabici w wypadkach",
        "Ranni w wypadkach",
    ]

    return police_data.loc[:, columns]


def fix_holidays_data(holidays_data: pd.DataFrame, year: int) -> pd.DataFrame:

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

    holidays_data = holidays_data.loc[:, columns_list]
    holidays_data.columns = columns_list
    holidays_data = holidays_data.reset_index(drop=True)
    holidays_data["Month"] = holidays_data["Date"].apply(
        lambda x: polish_months[x.split()[1]]
    )
    holidays_data["Day"] = holidays_data["Date"].apply(lambda x: int(x.split()[0]))
    holidays_data["Date"] = pd.to_datetime(
        str(year)
        + "-"
        + holidays_data["Month"].astype(str)
        + "-"
        + holidays_data["Day"].astype(str)
    )
    holidays_data.drop(columns=["Month", "Day"], inplace=True)
    return holidays_data
