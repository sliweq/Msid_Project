import os

import pandas as pd


def save_police_data_to_file(police_data: pd.DataFrame) -> None:
    """
    Save the police data to a CSV file in the 'project/data' directory.

    This function saves the police data to a CSV file in the 'project/data' directory.
    The file is named 'police_data.csv'.

    Args:
        police_data: DataFrame containing the police data.

    Returns:
        None
    """
    if os.path.exists(os.path.join("project", "data", "police_data.csv")):
        os.remove(os.path.join("project", "data", "police_data.csv"))
    police_data.to_csv(os.path.join("project", "data", "police_data.csv"), index=False)


def save_weather_data_to_file(weather_data: pd.DataFrame) -> None:
    """
    Save the weather data to a CSV file in the 'data' directory.

    This function saves the weather data to a CSV file in the 'project/data' directory.
    The file is named 'weather_data.csv'.

    Args:
        weather_data: DataFrame containing the weather data.

    Returns:
        None
    """
    if os.path.exists(os.path.join("project", "data", "weather_data.csv")):
        os.remove(os.path.join("project", "data", "weather_data.csv"))

    for file in os.listdir(os.path.join(os.getcwd(), "project", "data")):
        if file.endswith(".csv") and "k_d_" in file:
            os.remove(os.path.join(os.getcwd(), "project", "data", f"{file}"))

    weather_data.to_csv(
        os.path.join("project", "data", "weather_data.csv"), index=False
    )


def save_holidays_data_to_file(holidays_data: pd.DataFrame) -> None:
    """
    Save the holidays data to a CSV file in the 'data' directory.

    This function saves the holidays data to a CSV file in the 'data' directory.
    The file is named 'holidays_data.csv'.

    Args:
        holidays_data: DataFrame containing the holidays data.

    Returns:
        None
    """
    if os.path.exists(os.path.join("project", "data", "holidays_data.csv")):
        os.remove(os.path.join("project", "data", "holidays_data.csv"))

    holidays_data.to_csv(
        os.path.join("project", "data", "holidays_data.csv"), index=False
    )


def save_weekends_data_to_file(weekends_data: pd.DataFrame) -> None:
    """
    Save the weekends data to a CSV file in the 'data' directory.

    This function saves the weekends data to a CSV file in the 'data' directory.
    The file is named 'weekends_data.csv'.

    Args:
        weekends_data: DataFrame containing the weekends data.

    Returns:
        None
    """
    if os.path.exists(os.path.join("project", "data", "weekends_data.csv")):
        os.remove(os.path.join("project", "data", "weekends_data.csv"))
    weekends_data.to_csv(
        os.path.join("project", "data", "weekends_data.csv"), index=False
    )
