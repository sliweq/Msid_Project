import logging
import sys
from argparse import ArgumentParser, BooleanOptionalAction, Namespace

from project.data_processing.dataframes import read_csv_file
from project.data_processing.downloaders import download_data
from project.data_processing.models import prepare_model
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
    parser.add_argument(
        "values",
        metavar="N",
        type=float,
        nargs="*",
        default=[],
        help="Data used to predict: temperature, precipitation, weekends, holidays",
    )
    parser.add_argument(
        "-F",
        "--force",
        action=BooleanOptionalAction,
        default=False,
        help="Force download data",
    )
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    setup_logging()

    if args.force:
        download_data(2018, 2023)
        sys.exit(0)

    police_data = read_csv_file("police_data.csv")
    weather_data = read_csv_file("weather_data.csv")
    holidays_data = read_csv_file("holidays_data.csv")
    weekends_data = read_csv_file("weekends_data.csv")

    if args.visualization:
        visualize_data(police_data, weather_data)
    if args.statsistics:
        print_stats(police_data, weather_data, holidays_data, weekends_data)
    sys.exit(0)
    prediction = args.values
    if not prediction:
        prediction = [15, 3.1, 0, 0]
    if len(prediction) != 4:
        logger.error("Please provide 4 values to predict")
        sys.exit(1)

    prepare_model(
        police_data, weather_data, holidays_data, weekends_data, 2018, 2023, prediction
    )
    # prepare_model_1(police_data, weather_data, holidays_data, weekends_data, 2018, 2023)
