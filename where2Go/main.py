import forecast
import googlish
import sqlite3
import requests
from landmark import Landmark
import datetime

CATEGORIES_DB_NAMES = {
    '1': 'waterfalls',
    '2': 'lakes',
    '3': 'trails',
    '4': 'peaks'
}

CATEGORIES = {
    '1': 'водопади',
    '2': 'езера',
    '3': 'екопътеки',
    '4': 'върхове'
}

WEATHER_API_ID = 'ad5d3d8d3760a601675b4a38170c6f6a'


def read_and_fill(category):
    """
    Reads the information about the landmarks from the chosen category.
    Return a list of landmarks.
    """
    landmarks = []

    db_con = sqlite3.connect('landmarks.db')
    db = db_con.cursor()

    for row in db.execute('SELECT * FROM {}'.format(category)):
        # row[1] and row[2] - coordinates of the landmark
        forecast_data = get_forecast_info(row[1], row[2])

        if forecast_data['list'][1]['weather'][0]['main'] == 'Clear' or\
                forecast_data['list'][1]['weather'][0]['main'] == 'Clouds':
            landmarks.append(Landmark(row[0], row[1], row[2]))

            # was forecast_data['list'][1]['clouds']['all'] before
            # forecast_data['list'][1]['temp']['day']['main']
            landmarks[-1].set_forecast_data(
                forecast_data['list'][1]['clouds'],
                forecast_data['list'][1]['temp']['day'])
            duration = googlish.directions_and_durations.get_duration(
                row[1], row[2])
            landmarks[-1].set_travel_duration(duration)

    return landmarks


def get_forecast_info(lat, lon):
    """
    Sends http requests to the api for the exact location
    and return the response in json.
    """
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/forecast/daily?lat={}&lon={}&cnt=2&units=metric&APPID={}".format(
            lat, lon, WEATHER_API_ID))

    forecast_data = response.json()
    return forecast_data


def sort_landmarks(landmarks):
    """
    First sort the landmarks by the cloud percentage expectaion.
    After that sort them by temperature and after that by travel duration
    from the current position.
    """
    landmarks.sort(
        key=lambda landmark: landmark.get_cloud_percentage(), reverse=True)
    landmarks.sort(
        key=lambda landmark: landmark.get_average_temp(), reverse=True)
    landmarks.sort(
        key=lambda landmark: landmark.get_travel_duration())

    return landmarks


if __name__ == "__main__":
    print('''Моля, въведете цифра от 1 до 4:
    1: Водопади
    2: Езера
    3: Екопътеки
    4: Върхове''')

    while True:
        choice = input()
        if choice == '1' or choice == '2' or choice == '3' or choice == '4':
            print("Вие избрахте: {}".format(CATEGORIES[choice]))
            break
        else:
            print("Невалиден избор. Моля, въведете цифра между 1 и 4.")
            continue

    landmarks = read_and_fill(CATEGORIES_DB_NAMES[choice])
    if len(landmarks) != 0:
        landmarks_sorted = sort_landmarks(landmarks)
        for landmark in landmarks_sorted:
            print(
                landmark.get_name() + " - " +
                str(landmark.get_average_temp()) + " - " +
                str(landmark.get_cloud_percentage()) + " - " +
                str(datetime.timedelta(
                    seconds=landmark.get_travel_duration())))
    else:
        print("Няма места с хубаво време от избраната категория :(")
