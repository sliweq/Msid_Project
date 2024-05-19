import matplotlib.pyplot as plt
from data_processing.dataframes import Data
from pandas import DataFrame 

def police_data_chart(df: DataFrame) -> None:
    try:
        date = df['Data'].tolist()
        deaths = df['Zabici w wypadkach'].tolist()
        injured = df['Ranni w wypadkach'].tolist()
        accidents = df['Wypadki drogowe'].tolist()
    except TypeError:
        return
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(311)
    ax1.plot(date, deaths)
    ax1.plot(date, injured)
    ax1.plot(date, accidents)
    fig.suptitle('Police data')
    plt.show()

def police_deaths_chart(df: DataFrame) -> None:
    try: 
        date = df['Data'].tolist()
        deaths = df['Wypadki drogowe'].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5),sharey=True)
    axs.plot(date, deaths)
    fig.suptitle('Deaths in accidents')
    plt.show()

def police_injured_chart(df: DataFrame) -> None:
    try:
        date = df['Data'].tolist()
        injured = df['Ranni w wypadkach'].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5),sharey=True)
    axs.plot(date, injured)
    fig.suptitle('Injured in accidents')
    plt.show()

def police_accidents_chart(df: DataFrame) -> None:
    try:
        date = df['Data'].tolist()
        accidents = df['Wypadki drogowe'].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5),sharey=True)
    axs.plot(date, accidents)
    fig.suptitle('Accidents')
    plt.show()

def weather_temperature_chart(df : DataFrame) -> None: 
    try: 
        date = df['Date'].tolist()
        temp = df['Std Temp'].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5),sharey=True)
    axs.plot(date, temp)
    plt.axhline(0, color='gray', linestyle=':')
    plt.axhline(max(temp), color='red', linestyle='--')
    plt.axhline(min(temp), color='blue', linestyle='--')
    fig.suptitle('Average temperature')
    plt.show()

def weather_chart(df : DataFrame) -> None:
    try: 
        date = df['Date'].tolist()
        temp = df['Std Temp'].tolist()
        prec = df['Precip Sum'].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5),sharey=True)
    axs.plot(date, temp)
    axs.plot(date, prec)
    plt.axhline(0, color='gray', linestyle=':')
    plt.axhline(max(temp), color='red', linestyle='--')
    plt.axhline(min(temp), color='blue', linestyle='--')
    fig.suptitle('Weather')
    plt.show()

def precip_chart(df : DataFrame) -> None: 
    try: 
        date = df['Date'].tolist()
        prec = df['Precip Sum'].tolist()
    except TypeError:
        return
    fig, axs = plt.subplots(1, 1, figsize=(10, 5),sharey=True)
    axs.bar(date, prec)
    fig.suptitle('Precipitation')
    plt.show()
    
def snow_chart(df : DataFrame) -> None: 
    try: 
        date = df['Date'].tolist()
        prec = df['Precip Sum'].tolist()
        prec_type = df['Precip Type'].tolist()
    except TypeError:
        return
    prec = list(map(lambda x: x[0] if x[1] == 'S' else 0, zip(prec, prec_type)))
    fig, axs = plt.subplots(1, 1, figsize=(10, 5),sharey=True)
    axs.bar(date, prec)
    fig.suptitle('Snow precipitation')
    plt.show()

def rain_chart(df : DataFrame) -> None: 
    try: 
        date = df['Date'].tolist()
        prec = df['Precip Sum'].tolist()
        prec_type = df['Precip Type'].tolist()
    except TypeError:
        return
    prec = list(map(lambda x: x[0] if x[1] == 'W' else 0, zip(prec, prec_type)))
    fig, axs = plt.subplots(1, 1, figsize=(10, 5),sharey=True)
    axs.bar(date, prec)
    fig.suptitle('Rain precipitation')
    plt.show()