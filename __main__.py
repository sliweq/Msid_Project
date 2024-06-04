import logging

from data_processing.dataframes import *  # type: ignore # pylint: disable=import-error
from data_processing.downloaders import *  # type: ignore # pylint: disable=import-error
from data_processing.models import *  # type: ignore # pylint: disable=import-error
from data_processing.move_data import *  # type: ignore # pylint: disable=import-error
from data_processing.save_data import *
from setup_logging import \
    setup_logging  # type: ignore # pylint: disable=import-error
from visualization.tmp import *  # type: ignore # pylint: disable=import-error

logger = logging.getLogger()

if __name__ == "__main__":

    download_data(2018, 2023)

    police_data = read_csv_file("police_data.csv")
    weather_data = read_csv_file("weather_data.csv")
    holidays_data = read_csv_file("holidays_data.csv")
    weekends_data = read_csv_file("weekends_data.csv")
    # print(police_data.head())
    # print(weather_data.head())
    # print(holidays_data.head())
    # print(weekends_data.head())

    # visualize_data(police_data, weather_data)
    
    #24,6,26
    
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
    prepare_model_1(police_data, weather_data, holidays_data, weekends_data, 2018, 2023) 
    # 0.034704594593573966
    # 0.22493282915498927
    # 0.20848337169994482
    # [[56.11        7.75       65.89857143]]
    # [[55.50884026  5.02007403 64.16439149]]
    # [[53.71992457  4.57244931 61.05113727]]
    prepare_model_2(police_data, weather_data)  
    # 0.06169511044502
    # 0.23355600542863333
    # 0.21719083459596877
    # [[44.95    7.645  59.4025]]
    # [[37.96641334  4.59309534 47.25974581]]
    # [[40.53962101  4.47115829 48.34748976]]
    prepare_model_3(police_data, weather_data, holidays_data, 2018, 2023)  
    