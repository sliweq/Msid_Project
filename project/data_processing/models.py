import logging
from typing import Dict

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import make_scorer, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

from project.setup_logging import setup_logging

logger = logging.getLogger()
setup_logging()


def get_random_sum(series: DataFrame, count: int) -> int:
    """
    Calculates the sum of a random sample from a given series.

    Args:
        series (DataFrame): The series from which to draw the random sample.
        count (int): The number of elements to include in the random sample.

    Returns:
        int: The sum of the random sample.

    Raises:
        ValueError: If the count is greater than the length of the series.

    """
    if len(series) < count:
        raise ValueError("Count is bigger than series")
    return np.sum(np.random.choice(series, count, replace=False))  # type: ignore[no-any-return]


def prepare_model_svr(
    police: DataFrame,
    weather: DataFrame,
    holidays: DataFrame,
    weekends: DataFrame,
    start_year: int,
    end_year: int,
    prediction: list[float],
) -> None:
    """
    Prepare model for SVR regression.
    SVR use for prediction:
        -Average temperature
        -Precipitation sum
        -Weekends
        -Holidays
        -Last 3 days accidents
    """
    weather = weather.drop(columns=["Precip Type"])
    police = police.set_index("Data")

    police = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]

    police = police.join(weather.set_index("Date"))
    police = police.join(prepare_weekends(weekends, start_year, end_year))
    police = police.join(
        prepare_holidays(holidays.drop(columns=["Name"]), start_year, end_year)
    )
    police = police.dropna()
    shifted_accidents = police["Wypadki drogowe"].shift(1)
    police["last_3_days"] = shifted_accidents.rolling(window=3, min_periods=1).sum()
    police.iloc[0, police.columns.get_loc("last_3_days")] = get_random_sum(
        police["Wypadki drogowe"], 3
    )
    police.iloc[1, police.columns.get_loc("last_3_days")] += get_random_sum(
        police["Wypadki drogowe"], 2
    )
    police.iloc[2, police.columns.get_loc("last_3_days")] += get_random_sum(
        police["Wypadki drogowe"], 1
    )

    y = police[["Wypadki drogowe"]]

    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )
    run_svr(X, y, prediction, "Wypadki drogowe")
    y = police[["Zabici w wypadkach"]]
    run_svr(X, y, prediction, "Zabici w wypadkach")
    y = police[["Ranni w wypadkach"]]
    run_svr(X, y, prediction, "Ranni w wypadkach")


def prepare_model_rfr(
    police: DataFrame,
    weather: DataFrame,
    holidays: DataFrame,
    weekends: DataFrame,
    start_year: int,
    end_year: int,
    prediction: list[float],
) -> None:
    """
    Prepare model for Random Forest regression.
    Random Forest use for prediction:
        -Month
        -Weekday
        -Average temperature
        -Rain sum
        -Snow sum
        -Weekends
        -Holidays
        -Last 3 days accidents
    """
    police = police.set_index("Data")
    weather = weather.set_index("Date")
    weather["S"] = np.where(weather["Precip Type"] == "S", weather["Precip Sum"], 0)
    weather["W"] = np.where(weather["Precip Type"] == "W", weather["Precip Sum"], 0)

    police = police[["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]]
    police["Month"] = pd.to_datetime(police.index).month
    police["Week"] = pd.to_datetime(police.index).day_of_week

    police = police.join(weather.drop(columns=["Precip Type", "Precip Sum"]))
    police = police.join(prepare_weekends(weekends, start_year, end_year))
    police = police.join(
        prepare_holidays(holidays.drop(columns=["Name"]), start_year, end_year)
    )
    police = police.dropna()
    shifted_accidents = police["Wypadki drogowe"].shift(1)
    police["last_3_days"] = shifted_accidents.rolling(window=3, min_periods=1).sum()
    police.iloc[0, police.columns.get_loc("last_3_days")] = get_random_sum(
        police["Wypadki drogowe"], 3
    )
    police.iloc[1, police.columns.get_loc("last_3_days")] += get_random_sum(
        police["Wypadki drogowe"], 2
    )
    police.iloc[2, police.columns.get_loc("last_3_days")] += get_random_sum(
        police["Wypadki drogowe"], 1
    )

    y = police[["Wypadki drogowe"]]
    X = police.drop(
        columns=["Wypadki drogowe", "Zabici w wypadkach", "Ranni w wypadkach"]
    )
    run_rfr(X, y, prediction, "Wypadki drogowe")

    y = police[["Zabici w wypadkach"]]
    run_rfr(X, y, prediction, "Zabici w wypadkach")

    y = police[["Ranni w wypadkach"]]
    run_rfr(X, y, prediction, "Ranni w wypadkach")


def run_svr(
    X: DataFrame, y: DataFrame, to_predit: list[float], predcit_name: str
) -> None:
    """Run SVR model."""
    ct = ColumnTransformer(
        [("somename", StandardScaler(), ["Avg Temp", "Precip Sum", "last_3_days"])],
        remainder="passthrough",
    )
    X = ct.fit_transform(
        X[["Avg Temp", "Precip Sum", "Weekends", "Holidays", "last_3_days"]]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    svr = SVR(kernel="rbf", C=4, gamma=0.1)
    # svr = find_best_parameters(SVR(), {"C": [1, 2, 4], "gamma": [0.001 ,0.1, 1, 10]}, X_train, y_train)
    svr.fit(X_train, np.ravel(y_train))
    logger.info(f"SVR prediction for {predcit_name}")
    # logger.info(f"SVR parameters: {svr.get_params()}")
    logger.info(f"MAE: {mean_absolute_error(y_test, svr.predict(X_test))}")
    logger.info(f"SVR score: {svr.score(X_test, y_test)}")
    logger.info(
        f"SVR prediction for {to_predit}:{svr.predict(pd.DataFrame([to_predit]))}"
    )


def run_rfr(
    X: DataFrame, y: DataFrame, to_predit: list[float], predcit_name: str
) -> None:
    """Run Random Forest model."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    rfr = RandomForestRegressor(max_depth=7, n_estimators=100)
    # rfr = find_best_parameters(RandomForestRegressor(), {"n_estimators": [10, 100, 1000], "max_depth": [3,5,7]}, X_train, y_train)
    rfr.fit(X_train, np.ravel(y_train))

    to_predit_dict: Dict[str, float] = dict(zip(X.columns, to_predit))
    logger.info(f"Random forest regressor prediction for {predcit_name}")
    # logger.info(f"Random forest parameters: {rfr.get_params()}")
    logger.info(f"MAE: {mean_absolute_error(y_test, rfr.predict(X_test))}")
    logger.info(f"Random forest regressor score: {rfr.score(X_test, y_test)}")
    logger.info(
        f"Random forest regressor prediction for {to_predit_dict}:{rfr.predict(pd.DataFrame([to_predit_dict]))}"
    )


def find_best_parameters(model, parameters, X, y, verbose=2, n_jobs=-1):  # type: ignore[no-untyped-def]
    grid_object = GridSearchCV(
        model,
        parameters,
        scoring=make_scorer(r2_score),
        verbose=verbose,
        n_jobs=n_jobs,
        cv=10,
    )
    """Find best parameters for model."""
    grid_object = grid_object.fit(X, y)
    return grid_object.best_estimator_


def prepare_holidays(holidays: DataFrame, start_year: int, end_year: int) -> DataFrame:
    """Prepare holidays DataFrame for model."""
    date_range = pd.date_range(
        start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq="D"
    )
    df = pd.DataFrame(0, index=date_range, columns=["Holidays"])
    df.loc[holidays["Date"], "Holidays"] = 1
    return df


def prepare_weekends(weekends: DataFrame, start_year: int, end_year: int) -> DataFrame:
    """Prepare weekends DataFrame for model."""
    date_range = pd.date_range(
        start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq="D"
    )
    df = pd.DataFrame(0, index=date_range, columns=["Weekends"])
    df.loc[weekends["Date"], "Weekends"] = 1
    return df
