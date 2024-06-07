import pandas as pd
import numpy as np
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

def print_stats(police_data: pd.DataFrame, weather_data: pd.DataFrame, holidays_data: pd.DataFrame, weekends_data: pd.DataFrame) -> None:
    holidays_vs_normal_accidents(police_data, holidays_data)

def holidays_vs_normal_accidents(police_data: pd.DataFrame, holidays_data:pd.DataFrame) -> None:
    try:
        date = police_data["Data"].tolist()
        accidents = police_data["Wypadki drogowe"].tolist()
        holidays = holidays_data["Date"].tolist()
    except TypeError:
        return
    accidents_holiday = []
    print("Holidays vs normal accidents")
    for i in range(len(date)):
        if date[len(date)-i-1] in holidays:
            date.pop(len(date)-i-1)
            accidents_holiday.insert(0,accidents.pop(len(accidents)-i-1))
    
    print("Mean of accidents on holidays: ", np.mean(accidents_holiday))
    print("Mean of accidents on normal days: ", np.mean(accidents)) 

    

def weekends_vs_normal_accidents(police_data: pd.DataFrame, weekends_data:pd.DataFrame) -> None:
    pass

def weekends_vs_holidays_accidents(police_data: pd.DataFrame, holidays_data:pd.DataFrame,weekends_data:pd.DataFrame) -> None:
    pass

def holidays_stats(police_data: pd.DataFrame, holidays_data:pd.DataFrame) -> None:
    pass