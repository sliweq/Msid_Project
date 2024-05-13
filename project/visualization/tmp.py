import matplotlib.pyplot as plt
from data_processing.dataframes import Data
from pandas import DataFrame 
def police_stats_sum() -> None:
    pass

def police_deaths_chart() -> None:
    pass

def police_injured_chart() -> None:
    pass

def police_accidents_chart() -> None:
    pass

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