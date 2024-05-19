from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor  
from pandas import DataFrame
import pandas as pd
import joblib


def prepare_model(police:DataFrame ,weather:DataFrame, holidays:DataFrame,weekends: DataFrame) -> None:
    weather = weather.drop(columns=['Precip Type'])
    
    police = police.set_index('Data')
    weather = weather.set_index('Date')
    
    print(police.head())
    print(weather.head()) 
    print(holidays.head())
    print(weekends.head())
    

    police = police.join(weather)
    police = police.join(prepare_weekends(weekends,2022))
    police = police.join(prepare_holidays(holidays,2022))
    police = police.dropna()
    X = police.drop(columns=['Wypadki drogowe','Zabici w wypadkach','Ranni w wypadkach'])
    print(X.head())
    y = police['Wypadki drogowe']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
    joblib.dump(model, 'model.pkl')
    

def prepare_holidays(holidays:DataFrame, year : int) -> DataFrame:
    
    date_range = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31', freq='D')
    df = pd.DataFrame(0, index=date_range, columns=['Holidays'])
    df.loc[holidays['Date'], 'Holidays'] = 1
    print(df.head())
    return df

def prepare_weekends(weekends:DataFrame, year : int) -> DataFrame:
    
    date_range = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31', freq='D')
    df = pd.DataFrame(0, index=date_range, columns=['Weekends'])
    df.loc[weekends['Date'], 'Weekends'] = 1
    print(df.head())
    return df