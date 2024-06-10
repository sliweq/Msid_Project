import logging
from argparse import ArgumentParser, BooleanOptionalAction, Namespace

from project.data_processing.dataframes import read_csv_file
from project.data_processing.downloaders import download_data
from project.data_processing.models import prepare_model_rfr, prepare_model_svr
from project.setup import PREDICT_RFR, PREDICT_SVR
from project.setup_logging import setup_logging
from project.visualization.stats import print_stats
from project.visualization.visualization import visualize_data

logger = logging.getLogger()


def parse_args() -> Namespace:
    """Parse CLI arguments"""
    parser = ArgumentParser()
    parser.add_argument(
        "-V",
        "--visualization",
        action=BooleanOptionalAction,
        default=False,
        help="Visualize data",
    )
    parser.add_argument(
        "-S",
        "--statsistics",
        action=BooleanOptionalAction,
        default=False,
        help="Print statsistics",
    )
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    setup_logging()

    download_data(2018, 2023)

    police_data = read_csv_file("police_data.csv")
    weather_data = read_csv_file("weather_data.csv")
    holidays_data = read_csv_file("holidays_data.csv")
    weekends_data = read_csv_file("weekends_data.csv")

    if args.visualization:
        visualize_data(police_data, weather_data)
    if args.statsistics:
        print_stats(police_data, weather_data, holidays_data, weekends_data)

    prepare_model_svr(
        police_data,
        weather_data,
        holidays_data,
        weekends_data,
        2018,
        2023,
        PREDICT_SVR,
    )
    prepare_model_rfr(
        police_data,
        weather_data,
        holidays_data,
        weekends_data,
        2018,
        2023,
        PREDICT_RFR,
    )
