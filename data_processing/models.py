import joblib
import pandas as pd
import numpy as np
from pandas import DataFrame
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import (LinearRegression, LogisticRegression,
                                  LogisticRegressionCV)
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

def prepare_model_3(
    police: DataFrame,
    weather: DataFrame,
    weekends: DataFrame,
    start_year: int,
    end_year: int,
    ) -> None:
    """Model without holidays"""
    
    police = police.set_index("Data")
    weather = weather.set_index("Date")
    weather['S'] = np.where(weather['Precip Type'] == 'S', weather['Precip Sum'], 0)
    weather['W'] = np.where(weather['Precip Type'] == 'W', weather['Precip Sum'], 0)
    weather = weather.drop(columns=["Precip Type","Precip Sum"])
    
    police = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    police = police.join(weather)
    police = police.join(prepare_weekends(weekends, start_year, end_year))
    police = police.dropna()

    y = police[["Wypadki drogowe","Zabici w wypadkach","Ranni w wypadkach"]]

    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    model = MultiOutputRegressor(RandomForestRegressor(), n_jobs=-1)
    r = MultiOutputRegressor(LinearRegression(), n_jobs=-1)
    w = MultiOutputRegressor(SVR(kernel="linear"), n_jobs=-1)

    model.fit(X_train, y_train)
    r.fit(X_train, y_train)
    w.fit(X_train, y_train)

    print(model.score(X_test, y_test))
    print(r.score(X_test, y_test))
    print(w.score(X_test, y_test))

    t = {"Std Temp": [3], "S": [0.0], "W":[6.1], "Weekends": [1]}
    
    df = pd.DataFrame(t)

    print(model.predict(df))
    print(r.predict(df))
    print(w.predict(df))


def prepare_model_2(
    police: DataFrame,
    weather: DataFrame,
    ) -> None:
    """Model without weekends and holidays"""
    
    police = police.set_index("Data")
    weather = weather.set_index("Date")
    weather['S'] = np.where(weather['Precip Type'] == 'S', weather['Precip Sum'], 0)
    weather['W'] = np.where(weather['Precip Type'] == 'W', weather['Precip Sum'], 0)
    weather = weather.drop(columns=["Precip Type","Precip Sum"])
    
    police = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    police = police.join(weather)
    police = police.dropna()

    y = police[["Wypadki drogowe","Zabici w wypadkach","Ranni w wypadkach"]]

    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    model = MultiOutputRegressor(RandomForestRegressor(), n_jobs=-1)
    r = MultiOutputRegressor(LinearRegression(), n_jobs=-1)
    w = MultiOutputRegressor(SVR(kernel="linear"), n_jobs=-1)

    model.fit(X_train, y_train)
    r.fit(X_train, y_train)
    w.fit(X_train, y_train)


    print(model.score(X_test, y_test))
    print(r.score(X_test, y_test))
    print(w.score(X_test, y_test))

    t = {"Std Temp": [3], "S": [0.0], "W":[6.1]}

    df = pd.DataFrame(t)

    print(model.predict(df))
    print(r.predict(df))
    print(w.predict(df))


def prepare_model_1(
    police: DataFrame,
    weather: DataFrame,
    holidays: DataFrame,
    weekends: DataFrame,
    start_year: int,
    end_year: int,
    ) -> None:
    """Model with specified precipation type"""
    holidays = holidays.drop(columns=["Name"])
    police = police.set_index("Data")
    weather = weather.set_index("Date")
    weather['S'] = np.where(weather['Precip Type'] == 'S', weather['Precip Sum'], 0)
    weather['W'] = np.where(weather['Precip Type'] == 'W', weather['Precip Sum'], 0)
    weather = weather.drop(columns=["Precip Type","Precip Sum"])
    
    police = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    police = police.join(weather)
    police = police.join(prepare_weekends(weekends, start_year, end_year))
    police = police.join(prepare_holidays(holidays, start_year, end_year))
    police = police.dropna()

    y = police[["Wypadki drogowe","Zabici w wypadkach","Ranni w wypadkach"]]
    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    model = MultiOutputRegressor(RandomForestRegressor(), n_jobs=-1)
    r = MultiOutputRegressor(LinearRegression(), n_jobs=-1)
    w = MultiOutputRegressor(SVR(kernel="linear"), n_jobs=-1)

    model.fit(X_train, y_train)
    r.fit(X_train, y_train)
    w.fit(X_train, y_train)

    joblib.dump(model, "model.pkl")

    print(model.score(X_test, y_test))
    print(r.score(X_test, y_test))
    print(w.score(X_test, y_test))

    t = {"Std Temp": [3], "S": [0.0], "W":[6.1], "Weekends": [1], "Holidays": [1]}

    df = pd.DataFrame(t)

    print(model.predict(df))
    print(r.predict(df))
    print(w.predict(df))


def prepare_model(
    police: DataFrame,
    weather: DataFrame,
    holidays: DataFrame,
    weekends: DataFrame,
    start_year: int,
    end_year: int,
) -> None:
    """Model with all data"""
    weather = weather.drop(columns=["Precip Type"])
    holidays = holidays.drop(columns=["Name"])
    police = police.set_index("Data")
    weather = weather.set_index("Date")

    police = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    police = police.join(weather)
    police = police.join(prepare_weekends(weekends, start_year, end_year))
    police = police.join(prepare_holidays(holidays, start_year, end_year))
    police = police.dropna()

    y = police[["Wypadki drogowe","Zabici w wypadkach","Ranni w wypadkach"]]

    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    model = MultiOutputRegressor(RandomForestRegressor(), n_jobs=-1)
    r = MultiOutputRegressor(LinearRegression(), n_jobs=-1)
    w = MultiOutputRegressor(SVR(kernel="linear"), n_jobs=-1)

    model.fit(X_train, y_train)
    r.fit(X_train, y_train)
    w.fit(X_train, y_train)

    joblib.dump(model, "model.pkl")

    print(model.score(X_test, y_test))
    print(r.score(X_test, y_test))
    print(w.score(X_test, y_test))

    t = {"Std Temp": [3], "Precip Sum": [6.1], "Weekends": [1], "Holidays": [1]}
    df = pd.DataFrame(t)

    print(model.predict(df))
    print(r.predict(df))
    print(w.predict(df))


def prepare_holidays(holidays: DataFrame, start_year: int, end_year: int) -> DataFrame:

    date_range = pd.date_range(
        start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq="D"
    )
    df = pd.DataFrame(0, index=date_range, columns=["Holidays"])
    df.loc[holidays["Date"], "Holidays"] = 1
    return df


def prepare_weekends(weekends: DataFrame, start_year: int, end_year: int) -> DataFrame:

    date_range = pd.date_range(
        start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq="D"
    )
    df = pd.DataFrame(0, index=date_range, columns=["Weekends"])
    df.loc[weekends["Date"], "Weekends"] = 1
    return df
