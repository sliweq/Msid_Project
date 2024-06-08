import logging

from data_processing.dataframes import *  # type: ignore # pylint: disable=import-error
from data_processing.downloaders import *  # type: ignore # pylint: disable=import-error
from data_processing.models import *  # type: ignore # pylint: disable=import-error
from data_processing.move_data import *  # type: ignore # pylint: disable=import-error
from data_processing.save_data import *
from setup_logging import \
    setup_logging  # type: ignore # pylint: disable=import-error
from stats.stats import print_stats
from visualization.tmp import *  # type: ignore # pylint: disable=import-error

logger = logging.getLogger()

if __name__ == "__main__":

    # download_data(2018, 2023)

    police_data = read_csv_file("police_data.csv")
    weather_data = read_csv_file("weather_data.csv")
    holidays_data = read_csv_file("holidays_data.csv")
    weekends_data = read_csv_file("weekends_data.csv")

    # print(weekends_data.head())
    # print(holidays_data.head())
    # print(weather_data.head())
    # print_stats(police_data, weather_data, holidays_data, weekends_data)

    # profile = ProfileReport(police_data, title="Profiling Report")
    # profile.to_file("your_report.html")
    # visualize_data(police_data, weather_data)
    import sys

    from ydata_profiling import ProfileReport

    # sys.exit(0)
    # 24,6,26
    # 0.07220330791073637
    # 0.24075001020834552
    # 0.22527865366854247
    # [[40.6   7.47 51.62]]
    # [[36.4619728   4.96628203 47.37711603]]
    # [[38.44326847  4.52371914 48.58721264]]
    prepare_model(police_data, weather_data, holidays_data, weekends_data, 2018, 2023)
    # 0.06623621450650734
    # 0.24053407179608235
    # 0.2253297731212938
    # [[43.88  7.56 49.12]]
    # [[36.54501844  4.98623121 47.65340265]]
    # [[38.59690791  4.57261772 48.66534437]]

    # prepare_model_1(police_data, weather_data, holidays_data, weekends_data, 2018, 2023)
