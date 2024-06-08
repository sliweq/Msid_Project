import joblib
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import (LinearRegression, LogisticRegression,
                                  LogisticRegressionCV)
from sklearn.metrics import (classification_report, make_scorer, mean_absolute_error,
                             mean_squared_error)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.multioutput import MultiOutputRegressor, RegressorChain
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


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
    weather["S"] = np.where(weather["Precip Type"] == "S", weather["Precip Sum"], 0)
    weather["W"] = np.where(weather["Precip Type"] == "W", weather["Precip Sum"], 0)
    weather = weather.drop(columns=["Precip Type", "Precip Sum"])

    police = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    police = police.join(weather)
    police = police.join(prepare_weekends(weekends, start_year, end_year))
    police = police.join(prepare_holidays(holidays, start_year, end_year))
    police = police.dropna()

    y = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]
    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = MultiOutputRegressor(RandomForestRegressor(), n_jobs=-1)
    r = MultiOutputRegressor(LinearRegression(), n_jobs=-1)
    w = MultiOutputRegressor(SVR(kernel="linear"), n_jobs=-1)
    print(X.head())
    model.fit(X_train, y_train)
    r.fit(X_train, y_train)
    w.fit(X_train, y_train)

    joblib.dump(model, "model.pkl")

    print(model.score(X_test, y_test))
    print(r.score(X_test, y_test))
    print(w.score(X_test, y_test))

    t = {"Std Temp": [3.5], "S": [0.0], "W": [1.5], "Weekends": [0], "Holidays": [0]}

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

    y = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler

    # ct = ColumnTransformer([("somename",StandardScaler(),["Std Temp","Precip Sum"])],remainder='passthrough')
    # X = ct.fit_transform(X[["Std Temp","Precip Sum",  "Weekends" , "Holidays"]])
    # print(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    model = RandomForestRegressor()
    svm = SVR()
    # w = SVR(kernel="linear")
    # print(X.head())
    # model.fit(X_train, y_train)
    # parameters = {'C': [1.0, 2.0, 4.0], 
    #           'gamma': [0.001, 0.1, 1., 10.]
    #          }

    # svm = find_best_parameters(svm, parameters, X_train, y_train)
    
    # rbf, 10/0,001, 1/4/1
    svm = RandomForestRegressor(n_estimators=10, max_depth=1, bootstrap=True, n_jobs=-1)
    #svm = MultiOutputRegressor(SVR(kernel="rbf",C=4,gamma=10), n_jobs=-1)
    svm.fit(X_train, y_train)
    
    # w.fit(X_train, y_train)

    # joblib.dump(model, "model.pkl")

    # print(model.score(X_test, y_test))
    print(svm.score(X_test, y_test))
    # print(w.score(X_test, y_test))

    # t = {"Std Temp": [3.5], "Precip Sum": [1.5], "Weekends": [0], "Holidays": [0]}
    # df = pd.DataFrame(t)
    df = [[3.5, 1.5, 0, 0]]
    # print(model.predict(df))
    print(svm.predict(df))
    from sklearn.metrics import mean_absolute_error
    print(mean_absolute_error(y_test, svm.predict(X_test)))
    # print(w.predict(df))


def find_best_parameters(model, parameters, X, y, verbose=2, n_jobs=-1):
    grid_object = GridSearchCV(
        model,
        parameters,
        scoring=make_scorer(mean_absolute_error),
        verbose=verbose,
        n_jobs=n_jobs,
        cv=10,
    )
    print(y.head())
    grid_object = grid_object.fit(X, y)
    return grid_object.best_estimator_


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
