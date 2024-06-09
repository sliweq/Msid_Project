import logging
from venv import logger

import joblib
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn import svm
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import (LinearRegression, LogisticRegression,
                                  LogisticRegressionCV)
from sklearn.metrics import (classification_report, make_scorer,
                             mean_absolute_error, mean_squared_error)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

from project.setup_logging import setup_logging

if __name__ == "__main__":
    logger = logging.getLogger()
    setup_logging()


def prepare_model_1(
    police: DataFrame,
    weather: DataFrame,
    holidays: DataFrame,
    weekends: DataFrame,
    start_year: int,
    end_year: int,
    prediction: list[float],
) -> None:
    """Model with specified precipation type"""
    
    police = police.set_index("Data")
    weather = weather.set_index("Date")
    weather["S"] = np.where(weather["Precip Type"] == "S", weather["Precip Sum"], 0)
    weather["W"] = np.where(weather["Precip Type"] == "W", weather["Precip Sum"], 0)

    police = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    police = police.join(weather.drop(columns=["Precip Type", "Precip Sum"]))
    police = police.join(prepare_weekends(weekends, start_year, end_year))
    police = police.join(prepare_holidays(holidays.drop(columns=["Name"]), start_year, end_year))
    police = police.dropna()

    y = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]
    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )
    run_SVR_1(X, y, prediction)
    run_RandomForestRegressor(X, y, prediction)




def prepare_model(
    police: DataFrame,
    weather: DataFrame,
    holidays: DataFrame,
    weekends: DataFrame,
    start_year: int,
    end_year: int,
    prediction: list[float],
) -> None:
    """Model with all data"""
    weather = weather.drop(columns=["Precip Type"])
    police = police.set_index("Data")

    police = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    police = police.join(weather.set_index("Date"))
    police = police.join(prepare_weekends(weekends, start_year, end_year))
    police = police.join(
        prepare_holidays(holidays.drop(columns=["Name"]), start_year, end_year)
    )
    police = police.dropna()

    y = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )

    run_RandomForestRegressor(X, y, prediction)
    run_SVR(X, y, prediction)

def run_SVR_1(X: DataFrame, y: DataFrame, to_predit: list[float]) -> None:
    ct = ColumnTransformer(
        [("somename", StandardScaler(), ["Avg Temp", "W", "S"])],
        remainder="passthrough",
    )
    X = ct.fit_transform(X[["Avg Temp", "W", "S", "Weekends", "Holidays"]])
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    svr = SVR(kernel="rbf",C=1,gamma=0.001)
    mor = MultiOutputRegressor(svr, n_jobs=-1)
    mor.fit(X_train, y_train)
    
    logger.info(f"MAE: {mean_absolute_error(y_test, mor.predict(X_test))}")
    logger.info(f"SVR_1 score: {mor.score(X_test, y_test)}")
    logger.info(f"SVR_1 prediction for {to_predit}:{mor.predict(pd.DataFrame([to_predit]))}")

def run_SVR(X: DataFrame, y: DataFrame, to_predit: list[float]) -> None:
    ct = ColumnTransformer(
        [("somename", StandardScaler(), ["Avg Temp", "Precip Sum"])],
        remainder="passthrough",
    )
    X = ct.fit_transform(X[["Avg Temp", "Precip Sum", "Weekends", "Holidays"]])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    svr = SVR(kernel="rbf", C=4, gamma=10)

    mor = MultiOutputRegressor(svr, n_jobs=-1)
    mor.fit(X_train, y_train)

    logger.info(f"MAE: {mean_absolute_error(y_test, mor.predict(X_test))}")
    logger.info(f"SVR score: {mor.score(X_test, y_test)}")
    logger.info(f"SVR prediction for {to_predit}:{mor.predict(pd.DataFrame([to_predit]))}")



def run_RandomForestRegressor(
    X: DataFrame, y: DataFrame, to_predit: list[float]
) -> None:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    rfr = RandomForestRegressor(n_estimators=10, n_jobs=-1)

    rfr.fit(X_train, y_train)

    to_predit = dict(zip(X.columns, to_predit))
    logger.info(f"MAE: {mean_absolute_error(y_test, rfr.predict(X_test))}")
    logger.info(f"Random forest regressor score: {rfr.score(X_test, y_test)}")
    logger.info(f"Random forest regressor prediction for {to_predit}:{rfr.predict(pd.DataFrame([to_predit]))}")


def find_best_parameters(model, parameters, X, y, verbose=2, n_jobs=-1):
    grid_object = GridSearchCV(
        model,
        parameters,
        scoring=make_scorer(mean_absolute_error),
        verbose=verbose,
        n_jobs=n_jobs,
        cv=10,
    )

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
