from typing import Any, List

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from scipy.optimize import curve_fit
from scipy.stats import linregress


def sinusoidal(x, amplitude, frequency, phase, slope, intercept):  # type: ignore[no-untyped-def]
    """
    Calculate the value of a sinusoidal function at a given point.
    """
    return amplitude * np.sin(frequency * (x - phase)) + (slope * x + intercept)


def visualize_data(police_data: DataFrame, weather_data: DataFrame) -> None:
    """
    Visualizes the police data and weather data using various charts.

    Args:
        police_data (DataFrame): The police data to be visualized.
        weather_data (DataFrame): The weather data to be visualized.

    Returns:
        None
    """
    week_accidents_chart(police_data)
    years_accidents_chart(police_data)
    months_accidents_chart(police_data)
    police_accidents_chart(police_data)
    police_accidents_chart_sin(police_data)
    police_deaths_injured_chart(police_data)
    police_injured_chart_sin(police_data)
    police_death_chart_sin(police_data)
    weather_temperature_chart(weather_data)
    precip_chart(weather_data)
    rain_chart(weather_data)
    snow_chart(weather_data)


def week_accidents_chart(df: DataFrame) -> None:
    """
    Chart with accidents in days of week.
    """
    try:
        date = df["Data"].tolist()
        accidents = df["Wypadki drogowe"].tolist()
    except TypeError:
        return

    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    l: List[List[Any]] = [[] for _ in range(7)]
    for d, a in zip(date, accidents):
        l[d.weekday()].append(a)
    print([np.average(tmp) for tmp in l])
    axs.bar(list(range(1, 8)), [max(tmp) for tmp in l])
    axs.bar(list(range(1, 8)), [np.average(tmp) for tmp in l])
    axs.bar(list(range(1, 8)), [min(tmp) for tmp in l])
    plt.title("Accidents in days of week")
    plt.xlabel("Day of week 1-Monday, 7-Sunday")
    plt.ylabel("Number of accidents")
    plt.legend(["Max", "Mean", "Min"])
    plt.show()


def years_accidents_chart(df: DataFrame) -> None:
    """
    Chart with accidents per years.
    """
    try:
        date = df["Data"].tolist()
        accidents = df["Wypadki drogowe"].tolist()
    except TypeError:
        return

    years = [2018, 2019, 2020, 2021, 2022, 2023]
    fig, axs = plt.subplots(2, 3, figsize=(10, 5), sharey=True)
    for i, year in enumerate(years):
        list_years = [
            list(t)
            for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.year == year])
        ]
        axs[i // 3, i % 3].plot(list_years[0], list_years[1])
    plt.title("Accidents per year")
    plt.show()


def months_accidents_chart(df: DataFrame) -> None:
    """
    Charts with accidents per month.
    """
    try:
        date = df["Data"].tolist()
        accidents = df["Wypadki drogowe"].tolist()
    except TypeError:
        return

    fig, axs = plt.subplots(2, 6, figsize=(10, 5), sharey=True)
    list_month = [
        list(t) for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 1])
    ]
    axs[0, 0].scatter(list_month[0], list_month[1])
    list_month = [
        list(t) for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 2])
    ]
    axs[0, 1].scatter(list_month[0], list_month[1])
    list_month = [
        list(t) for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 3])
    ]
    axs[0, 2].scatter(list_month[0], list_month[1])
    list_month = [
        list(t) for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 4])
    ]
    axs[0, 3].scatter(list_month[0], list_month[1])
    list_month = [
        list(t) for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 5])
    ]
    axs[0, 4].scatter(list_month[0], list_month[1])
    list_month = [
        list(t) for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 6])
    ]
    axs[0, 5].scatter(list_month[0], list_month[1])
    list_month = [
        list(t) for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 7])
    ]
    axs[1, 0].scatter(list_month[0], list_month[1])
    list_month = [
        list(t) for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 8])
    ]
    axs[1, 1].scatter(list_month[0], list_month[1])
    list_month = [
        list(t) for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 9])
    ]
    axs[1, 2].scatter(list_month[0], list_month[1])
    list_month = [
        list(t)
        for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 10])
    ]
    axs[1, 3].scatter(list_month[0], list_month[1])
    list_month = [
        list(t)
        for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 11])
    ]
    axs[1, 4].scatter(list_month[0], list_month[1])
    list_month = [
        list(t)
        for t in zip(*[[d, a] for d, a in zip(date, accidents) if d.month == 12])
    ]
    axs[1, 5].scatter(list_month[0], list_month[1])
    plt.title("Accidents per month")
    plt.show()


def police_death_chart_sin(df: DataFrame) -> None:
    """
    Chart with deaths in accidents.
    """
    try:
        deaths = df["Zabici w wypadkach"].tolist()
    except TypeError:
        return

    x = np.linspace(0, len(df["Data"]) + 1, len(df["Data"]))

    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(311)

    ax1.plot(x, deaths)
    plt.xlabel("Date")
    plt.ylabel("Deaths")

    fig.suptitle("Death chart")
    plt.show()


def police_injured_chart_sin(df: DataFrame) -> None:
    """
    Chart with injured in accidents and sin.
    """
    try:
        injured = df["Ranni w wypadkach"].tolist()
    except TypeError:
        return

    x = np.linspace(0, len(df["Data"]) + 1, len(df["Data"]))
    slope, intercept, r_value, p_value, std_err = linregress(x, injured)

    regression_line = slope * x + intercept
    print(f"Regression line for injured: {slope}*x+{intercept}")

    initial_guess = [20, 0.02, 0, slope, intercept]
    params, params_covariance = curve_fit(sinusoidal, x, injured, p0=initial_guess)

    fitted_accidents = sinusoidal(x, *params)

    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(311)

    ax1.plot(x, injured, label="Dane")
    ax1.plot(x, fitted_accidents, label="Fitted func")

    plt.xlabel("Date")
    plt.plot(x, regression_line, label="Regression line", color="red")

    fig.suptitle("Injured with sin and regression line")
    plt.show()


def police_accidents_chart_sin(df: DataFrame) -> None:
    """
    Chart with amount of accidents and sin.
    """
    try:
        accidents = df["Wypadki drogowe"].tolist()
    except TypeError:
        return

    x = np.linspace(0, len(df["Data"]) + 1, len(df["Data"]))

    slope, intercept, r_value, p_value, std_err = linregress(x, accidents)
    regression_line = slope * x + intercept
    # y = 20*np.sin(0.0173*(x-120))+(slope * x + intercept)
    print(f"Regression line for accidents: {slope}*x+{intercept}")

    initial_guess = [20, 0.02, 0, slope, intercept]

    params, params_covariance = curve_fit(sinusoidal, x, accidents, p0=initial_guess)

    fitted_accidents = sinusoidal(x, *params)

    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(311)

    ax1.plot(x, accidents, label="Dane")
    ax1.plot(x, fitted_accidents, label="Fitted func")

    plt.xlabel("Date")
    plt.plot(x, regression_line, label="Regression line", color="red")

    fig.suptitle("Accidents with sin and regression line")
    plt.show()


def police_data_chart(df: DataFrame) -> None:
    """
    All police data in one chart.
    """
    try:
        date = df["Data"].tolist()
        deaths = df["Zabici w wypadkach"].tolist()
        injured = df["Ranni w wypadkach"].tolist()
        accidents = df["Wypadki drogowe"].tolist()
    except TypeError:
        return
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(311)
    ax1.plot(date, deaths)
    ax1.plot(date, injured)
    ax1.plot(date, accidents)
    plt.axhline(0, color="gray", linestyle=":")
    plt.axhline(max(deaths), color="black", linestyle="--")
    plt.axhline(max(accidents), color="red", linestyle="--")
    plt.xlabel("Date")
    ax1.legend(["Deaths", "Injured", "Accidents"])
    fig.suptitle("Police data")
    plt.show()


def police_deaths_injured_chart(df: DataFrame) -> None:
    """
    Police data with deaths and injured in accidents.
    """
    try:
        date = df["Data"].tolist()
        deaths = df["Zabici w wypadkach"].tolist()
        injured = df["Ranni w wypadkach"].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    axs.plot(date, deaths)
    axs.plot(date, injured)
    plt.axhline(0, color="gray", linestyle=":")
    plt.axhline(max(deaths), color="black", linestyle="--")
    plt.axhline(max(injured), color="red", linestyle="--")
    axs.legend(["Deaths", "Injured"])
    fig.suptitle("Deaths and injured in accidents")
    plt.show()


def police_deaths_chart(df: DataFrame) -> None:
    """
    Police data with deaths in accidents.
    """
    try:
        date = df["Data"].tolist()
        deaths = df["Wypadki drogowe"].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    axs.plot(date, deaths)
    fig.suptitle("Deaths in accidents")
    plt.show()


def police_injured_chart(df: DataFrame) -> None:
    """
    Police data with injured in accidents.
    """

    try:
        date = df["Data"].tolist()
        injured = df["Ranni w wypadkach"].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    axs.plot(date, injured)
    fig.suptitle("Injured in accidents")
    plt.show()


def police_accidents_chart(df: DataFrame) -> None:
    """
    Chart with accidents.
    """

    try:
        date = df["Data"].tolist()
        accidents = df["Wypadki drogowe"].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    axs.plot(date, accidents)
    fig.suptitle("Accidents")
    plt.xlabel("Date")
    plt.ylabel("Number of accidents")
    plt.show()


def weather_temperature_chart(df: DataFrame) -> None:
    """
    Chart with avg temperature.
    """

    try:
        date = df["Date"].tolist()
        temp = df["Avg Temp"].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    axs.plot(date, temp)
    plt.axhline(0, color="gray", linestyle=":")
    plt.axhline(max(temp), color="red", linestyle="--")
    plt.axhline(min(temp), color="blue", linestyle="--")
    fig.suptitle("Average temperature")
    plt.xlabel("Date")
    plt.ylabel("Temperature in Celsius")
    plt.show()


def weather_chart(df: DataFrame) -> None:
    """
    All weather data on one chart.
    """
    try:
        date = df["Date"].tolist()
        temp = df["Avg Temp"].tolist()
        prec = df["Precip Sum"].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    axs.plot(date, temp, color="red")
    axs.plot(date, prec, color="blue")
    plt.axhline(0, color="gray", linestyle=":")
    plt.axhline(max(temp), color="red", linestyle="--")
    plt.axhline(min(temp), color="red", linestyle="--")
    plt.axhline(max(prec), color="blue", linestyle="--")
    plt.axhline(min(prec), color="blue", linestyle="--")
    axs.legend(["Temperature", "Precipitation"])
    fig.suptitle("Weather")

    plt.show()


def precip_chart(df: DataFrame) -> None:
    """
    Chart with precipitation.
    """
    try:
        date = df["Date"].tolist()
        prec = df["Precip Sum"].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    axs.bar(date, prec)
    plt.ylabel("Precipitation in mm/m^2")
    plt.xlabel("Date")
    fig.suptitle("Precipitation")
    plt.show()


def snow_chart(df: DataFrame) -> None:
    """
    Chart with snow precipitation.
    """
    try:
        date = df["Date"].tolist()
        prec = df["Precip Sum"].tolist()
        prec_type = df["Precip Type"].tolist()
    except TypeError:
        return
    prec = list(map(lambda x: x[0] if x[1] == "S" else 0, zip(prec, prec_type)))
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    axs.bar(date, prec)
    plt.xlabel("Date")
    plt.ylabel("Precipitation in mm/m^2")
    fig.suptitle("Snow precipitation")
    plt.show()


def rain_chart(df: DataFrame) -> None:
    """
    Chart with rain precipitation.
    """
    try:
        date = df["Date"].tolist()
        prec = df["Precip Sum"].tolist()
        prec_type = df["Precip Type"].tolist()
    except TypeError:
        return
    prec = list(map(lambda x: x[0] if x[1] == "W" else 0, zip(prec, prec_type)))
    fig, axs = plt.subplots(1, 1, figsize=(10, 5), sharey=True)
    axs.bar(date, prec)
    plt.xlabel("Date")
    plt.ylabel("Precipitation in mm/m^2")
    fig.suptitle("Rain precipitation")
    plt.show()
