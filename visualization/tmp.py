from turtle import color

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from scipy.stats import linregress
from scipy.optimize import curve_fit

def sinusoidal(x, amplitude, frequency, phase, offset, slope, intercept):
        return amplitude * np.sin(frequency * (x - phase)) + (slope * x + intercept)

def visualize_data(police_data: DataFrame, weather_data: DataFrame) -> None:
    police_accidents_chart(police_data)
    police_accidents_chart_sin(police_data)
    police_deaths_injured_chart(police_data)
    police_injured_chart_sin(police_data)
    police_death_chart_sin(police_data)
    weather_temperature_chart(weather_data)
    precip_chart(weather_data)
    rain_chart(weather_data)
    snow_chart(weather_data)


def police_death_chart_sin(df: DataFrame) -> None:
    try:
        deaths = df["Zabici w wypadkach"].tolist()
    except TypeError:
        return

    x = np.linspace(0, len(df['Data'])+1, len(df['Data']))
    
    slope, intercept, r_value, p_value, std_err = linregress(x, deaths)
    regression_line = slope * x + intercept
    print(f"Regression line for injured: {slope}*x+{intercept}")
    
    initial_guess = [20, 0.02, 0, 0,slope,intercept]
    params, params_covariance = curve_fit(sinusoidal, x, deaths, p0=initial_guess)
    fitted_accidents = sinusoidal(x, *params)
    
    
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(311)

    
    ax1.plot(x, deaths)
    plt.xlabel("Date")
    plt.ylabel("Deaths")
    plt.plot(x, regression_line, label='Regression line', color='red')
    
    ax1.plot(x, fitted_accidents, label='Fitted func')    
    
    fig.suptitle("Death chart with sin and regression line")
    plt.show()
    


def police_injured_chart_sin(df: DataFrame) -> None:
    try:
        injured = df["Ranni w wypadkach"].tolist()
    except TypeError:
        return

    x = np.linspace(0, len(df['Data'])+1, len(df['Data']))    
    slope, intercept, r_value, p_value, std_err = linregress(x, injured)
    
    
    regression_line = slope * x + intercept
    print(f"Regression line for injured: {slope}*x+{intercept}")
    
    initial_guess = [20, 0.02, 0, 0,slope,intercept]
    params, params_covariance = curve_fit(sinusoidal, x, injured, p0=initial_guess)

    fitted_accidents = sinusoidal(x, *params)
    
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(311)

    
    ax1.plot(x, injured, label='Dane')
    ax1.plot(x, fitted_accidents, label='Fitted func')    
    
    plt.xlabel("Date")
    plt.plot(x, regression_line, label='Regression line', color='red')
    
    fig.suptitle("Injured with sin and regression line")
    plt.show()  
    

def police_accidents_chart_sin(df: DataFrame) -> None:
    try:
        accidents = df["Wypadki drogowe"].tolist()
    except TypeError:
        return

    x = np.linspace(0, len(df['Data'])+1, len(df['Data']))
    
    slope, intercept, r_value, p_value, std_err = linregress(x, accidents)
    regression_line = slope * x + intercept
    # y = 20*np.sin(0.0173*(x-120))+(slope * x + intercept)
    print(f"Regression line for accidents: {slope}*x+{intercept}")
    
    initial_guess = [20, 0.02, 0, 0,slope,intercept]
    
    params, params_covariance = curve_fit(sinusoidal, x, accidents, p0=initial_guess)


    fitted_accidents = sinusoidal(x, *params)
    
    
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(311)
    
    ax1.plot(x, accidents, label='Dane')
    ax1.plot(x, fitted_accidents, label='Fitted func')    
    
    plt.xlabel("Date")
    plt.plot(x, regression_line, label='Regression line', color='red')
    
    fig.suptitle("Accidents with sin and regression line")
    plt.show()

def police_data_chart(df: DataFrame) -> None:
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
    try:
        date = df["Date"].tolist()
        temp = df["Std Temp"].tolist()
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
    try:
        date = df["Date"].tolist()
        temp = df["Std Temp"].tolist()
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
