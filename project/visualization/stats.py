from cProfile import label
from math import floor

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import axes
from scipy.stats import linregress

#         Date
# 0 2018-01-05
# 1 2018-01-06
# 2 2018-01-07
# 3 2018-01-12
# 4 2018-01-13
#         Date                 Name
# 0 2018-01-01       New Year's Day
# 1 2018-01-06             Epiphany
# 2 2018-04-01        Easter Sunday
# 3 2018-04-02        Easter Monday
# 4 2018-05-01  Labor Day / May Day


def print_stats(
    police_data: pd.DataFrame,
    weather_data: pd.DataFrame,
    holidays_data: pd.DataFrame,
    weekends_data: pd.DataFrame,
) -> None:

    temperature_accidents_regress(police_data, weather_data)
    temperature_accidents(police_data, weather_data)
    normal_vs_rest(police_data, holidays_data, weekends_data)
    normal_vs_rain(police_data, weather_data)
    normal_vs_rain_vs_snow(police_data, weather_data)


def normal_vs_rest(
    police_data: pd.DataFrame, holidays_data: pd.DataFrame, weekends_data: pd.DataFrame
) -> None:
    try:
        date = police_data["Data"].tolist()
        accidents = police_data["Wypadki drogowe"].tolist()

        holidays = holidays_data["Date"].tolist()
        weekends = weekends_data["Date"].tolist()
    except TypeError:
        return
    accidents_holiday = []
    accidents_weekend = []

    for i in range(len(date)):
        if len(date) - i - 1 >= 0:
            if date[len(date) - i - 1] in holidays:
                date.pop(len(date) - i - 1)
                accident = accidents.pop(len(accidents) - i - 1)
                accidents_holiday.insert(0, accident)
                if len(date) - i - 1 >= 0 and date[len(date) - i - 1] in weekends:
                    accidents_weekend.insert(0, accident)
                date.pop(len(date) - i - 1)

            if len(date) - i - 1 >= 0 and date[len(date) - i - 1] in weekends:
                date.pop(len(date) - i - 1)
                accident = accidents.pop(len(accidents) - i - 1)
                accidents_weekend.insert(0, accident)
                if len(date) - i - 1 >= 0 and date[len(date) - i - 1] in holidays:
                    accidents_holiday.insert(0, accident)
                date.pop(len(date) - i - 1)

    types = ["Normal days", "Holidays", "Weekends"]

    fig, ax = plt.subplots()
    ax.bar(
        types,
        [np.max(accidents), np.max(accidents_holiday), np.max(accidents_weekend)],
        label="Max",
    )
    ax.bar(
        types,
        [np.mean(accidents), np.mean(accidents_holiday), np.mean(accidents_weekend)],
        yerr=[np.std(accidents), np.std(accidents_holiday), np.std(accidents_weekend)],
        label="Mean",
    )
    print([np.std(accidents), np.std(accidents_holiday), np.std(accidents_weekend)])
    ax.bar(
        types,
        [np.min(accidents), np.min(accidents_holiday), np.min(accidents_weekend)],
        label="Min",
    )
    plt.ylabel("Mean Number of Accidents")
    ax.legend()
    plt.show()


def normal_vs_rain(police_data: pd.DataFrame, weather_data: pd.DataFrame) -> None:
    try:
        date = police_data["Data"].tolist()
        accidents = police_data["Wypadki drogowe"].tolist()

        rain = weather_data["Precip Sum"].tolist()
    except TypeError:
        return

    accidents_rain = []
    for i in range(len(date)):
        if rain[len(date) - i - 1] > 0:
            accidents_rain.append(accidents.pop(len(date) - i - 1))

    types = ["Normal days", "Rainy days"]
    fig, ax = plt.subplots()
    ax.bar(
        types,
        [np.max(accidents), np.max(accidents_rain)],
        label="Max",
    )
    ax.bar(
        types,
        [np.mean(accidents), np.mean(accidents_rain)],
        yerr=[np.std(accidents), np.std(accidents_rain)],
        label="Mean",
    )
    ax.bar(
        types,
        [np.min(accidents), np.min(accidents_rain)],
        label="Min",
    )
    plt.ylabel("Mean Number of Accidents")
    ax.legend()
    plt.show()


def normal_vs_rain_vs_snow(
    police_data: pd.DataFrame, weather_data: pd.DataFrame
) -> None:
    try:
        date = police_data["Data"].tolist()
        accidents = police_data["Wypadki drogowe"].tolist()

        precip = weather_data["Precip Sum"].tolist()
        precip_type = weather_data["Precip Type"].tolist()
    except TypeError:
        return

    accidents_rain = []
    accidents_snow = []
    for i in range(len(date)):
        if precip[len(date) - i - 1] > 0:
            if precip_type[len(date) - i - 1] == "S":
                accidents_snow.append(accidents.pop(len(date) - i - 1))
            else:
                accidents_rain.append(accidents.pop(len(date) - i - 1))

    types = ["Normal days", "Rainy days", "Snowy days"]
    fig, ax = plt.subplots()
    ax.bar(
        types,
        [np.max(accidents), np.max(accidents_rain), np.max(accidents_snow)],
        label="Max",
    )
    ax.bar(
        types,
        [np.mean(accidents), np.mean(accidents_rain), np.mean(accidents_snow)],
        yerr=[np.std(accidents), np.std(accidents_rain), np.std(accidents_snow)],
        label="Mean",
    )
    ax.bar(
        types,
        [np.min(accidents), np.min(accidents_rain), np.min(accidents_snow)],
        label="Min",
    )
    plt.ylabel("Mean Number of Accidents")
    ax.legend()
    plt.show()


def temperature_accidents(
    police_data: pd.DataFrame, weather_data: pd.DataFrame
) -> None:
    try:
        date = police_data["Data"].tolist()
        accidents = police_data["Wypadki drogowe"].tolist()

        temperature = weather_data["Std Temp"].tolist()
    except TypeError:
        return

    accidents_temperature = {}
    for i in range(len(date)):
        if floor(temperature[len(date) - i - 1]) not in accidents_temperature.keys():
            accidents_temperature[floor(temperature[len(date) - i - 1])] = []

        accidents_temperature[floor(temperature[len(date) - i - 1])].append(
            accidents.pop(len(date) - i - 1)
        )

    fig, ax = plt.subplots()
    ax.bar(
        accidents_temperature.keys(),
        [np.max(i) for i in accidents_temperature.values()],
        label="Max",
    )
    ax.bar(
        accidents_temperature.keys(),
        [np.mean(i) for i in accidents_temperature.values()],
        yerr=[np.std(i) for i in accidents_temperature.values()],
        label="Mean",
    )
    ax.bar(
        accidents_temperature.keys(),
        [np.min(i) for i in accidents_temperature.values()],
        label="Min",
    )
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Mean Number of Accidents")
    plt.legend()
    plt.show()


def temperature_accidents_regress(
    police_data: pd.DataFrame, weather_data: pd.DataFrame
) -> None:
    try:
        date = police_data["Data"].tolist()
        accidents = police_data["Wypadki drogowe"].tolist()

        temperature = weather_data["Std Temp"].tolist()
    except TypeError:
        return

    accidents_temperature = {}
    for i in range(len(date)):
        if floor(temperature[len(date) - i - 1]) not in accidents_temperature.keys():
            accidents_temperature[floor(temperature[len(date) - i - 1])] = []

        accidents_temperature[floor(temperature[len(date) - i - 1])].append(
            accidents.pop(len(date) - i - 1)
        )

    fig, ax = plt.subplots()

    ax.bar(
        accidents_temperature.keys(),
        [np.mean(i) for i in accidents_temperature.values()],
        label="Mean",
    )

    slope, intercept, r_value, p_value, std_err = linregress(
        list(accidents_temperature.keys()),
        [np.mean(i) for i in accidents_temperature.values()],
    )
    regression_line = int(slope) * list(accidents_temperature.keys()) + intercept

    plt.plot(
        accidents_temperature.keys(),
        regression_line,
        label="Regression line",
        color="red",
    )
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Mean Number of Accidents")
    plt.legend()
    plt.show()
