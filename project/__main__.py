import logging

from data_processing.dataframes import * # type: ignore # pylint: disable=import-error
from data_processing.downloaders import * # type: ignore # pylint: disable=import-error
from data_processing.move_data import *  # type: ignore # pylint: disable=import-error
from setup_logging import \
    setup_logging  # type: ignore # pylint: disable=import-error
from data_processing.models import *  # type: ignore # pylint: disable=import-error
from visualization.tmp import *  # type: ignore # pylint: disable=import-error

logger = logging.getLogger()

if __name__ == "__main__":
    setup_logging()
    # p = PoliceDataDownloader()
    # p.download(2022)
    # d = Data(police_data=p.get_data(), holidays_data=None, weekends=None, weather=None, year=2022)
    # d.fix_police_data()
    # save_police_data_to_file(d.police_data)
    
    # d = Data(police_data=read_police_data_from_cvs(), holidays_data=None, weekends=None, weather=None, year=2022)
    
    # police_deaths_chart(d.police_data)
    # police_accidents_chart(d.police_data)
    # police_injured_chart(d.police_data)
    # police_data_chart(d.police_data)

    # w = WeatherDataDownloader(2022)
    # w.download()
    # move_zip_files()
    # unzip_files()
    # delete_useless_files()
    
    # weather_chart(create_weather_dataframe())
    
    # weather = create_weather_dataframe()
    # weather_temperature_chart(create_weather_dataframe())
    # precip_chart(create_weather_dataframe())
    # snow_chart(create_weather_dataframe())
    # rain_chart(create_weather_dataframe())
    
    # data = p.get_data()
    # for i,n in data.iterrows():
    #     print(i)
    #     print(n["Data"])

    # print(create_weekends_dataframe(2023))

    # d = Data(policeData=p.get_data(), holidaysData=None, weekends=None, year=2024)

    # d.fix_police_data()
    # print(d.policeData)

    h = HolidaysDataDownloader()
    h.download(2022)
    d = Data(police_data=read_police_data_from_cvs(), holidays_data=h.get_data(), weekends=create_weekends_dataframe(2022),weather=create_weather_dataframe() ,year=2022)
    d.fix_holidays_data()    
    d.fix_police_data()
    
    prepare_model(police=d.police_data,weather=d.weather,holidays=d.holidays_data,weekends=d.weekends)
    
    import joblib
    model = joblib.load("model.pkl")
    data = {
    'Date': ['2024-05-02'],  # Przyjmujemy, że jest to rok 2024
    'Std Temp': [30],      # Średnia temperatura w stopniach Celsjusza
    'Precip Sum': [4.2],   # Opady w mm
    'Weekends': [1],       # Zakładamy, że 2 maja jest weekendem
    'Holidays': [0],        # Zakładamy, że 2 maja nie jest świętem
    }
    
    df_new = pd.DataFrame(data)

    # Przetwarzanie kolumny 'date' do formatu datetime
    df_new['Date'] = pd.to_datetime(df_new['Date'])
    
    X_new = df_new[['Std Temp', 'Precip Sum','Weekends', 'Holidays']]
    predicted_accidents = model.predict(X_new)
    print(f'Przewidywana liczba wypadków: {predicted_accidents[0]}')

    
    