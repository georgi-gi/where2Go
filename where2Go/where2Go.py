import googlish
import sqlite3
import requests
from landmark import Landmark
from datetime import datetime
from datetime import timedelta

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


def read_and_fill(category, current_or_address, address, days):
    """
    Reads the information about the landmarks from the chosen category.
    Return a list of landmarks.
    """
    landmarks = []

    db_con = sqlite3.connect('landmarks.db')
    db = db_con.cursor()

    for row in db.execute('SELECT * FROM {}'.format(category)):
        # row[1] and row[2] - coordinates of the landmark
        forecast_data = get_forecast_info(row[1], row[2], days)

        if forecast_data['list'][days - 1]['weather'][0]['main'] == 'Clear' or\
                forecast_data['list'][days - 1]['weather'][0]['main'] == \
                'Clouds':
            landmarks.append(Landmark(row[0], row[1], row[2]))

            # was forecast_data['list'][1]['clouds']['all'] before
            # forecast_data['list'][1]['temp']['day']['main']
            landmarks[-1].set_forecast_data(
                forecast_data['list'][days - 1]['clouds'],
                forecast_data['list'][days - 1]['temp']['day'])

            if current_or_address == '1':
                duration = googlish.directions_and_durations.get_duration(
                    row[1], row[2])
                landmarks[-1].set_travel_duration(duration)
            else:
                duration = googlish.directions_and_durations.\
                    get_duration_from_address(address, row[1], row[2])
                landmarks[-1].set_travel_duration(duration)

    return landmarks


def get_forecast_info(lat, lon, days):
    """
    Sends http requests to the weather api for the exact location
    and return the response in json.
    """
    url = ("http://api.openweathermap.org/data/"
           "2.5/forecast/daily?lat={}&lon={}&cnt={}"
           "&units=metric&APPID={}").format(lat, lon, days, WEATHER_API_ID)
    response = requests.get(url)

    forecast_data = response.json()
    return forecast_data


def enter_date():
    isValid = False
    while not isValid:
        user_date = input(
            "Моля, въведете дата от следващите 16 дни(дд/мм/гг): ")
        try:
            date = datetime.strptime(user_date, "%d/%m/%y")
            current_day = datetime.now()
            delta = date - current_day
            if delta.days >= 0 and delta.days <= 16:
                isValid = True
        except:
            print("Невалиден формат на датата или твърде далечна.")

    return delta.days


def sort_landmarks(landmarks):
    """
    First sorts the landmarks by the cloud percentage expectaion.
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
    while True:
        print('''Моля, въведете цифра от 1 до 4:
        1: Водопади
        2: Езера
        3: Екопътеки
        4: Върхове''')

        while True:
            choice = input()
            if choice == '1' or choice == '2' or\
                    choice == '3' or choice == '4':
                print("Вие избрахте: {}".format(CATEGORIES[choice]))
                break
            else:
                print("Невалиден избор. Моля, въведете цифра между 1 и 4.")
                continue

        date = enter_date()

        address = None
        current_or_not = '0'
        while current_or_not != '1' and current_or_not != '2':
            print('''Изчисленията да са спрямо:
                1 - сегашната ми позиция
                2 - избран от мен адрес''')
            current_or_not = input()

        if current_or_not == '2':
            address = input("Моля, въведете адрес: ")
            address = address.replace(" ", "+")

        landmarks = read_and_fill(
            CATEGORIES_DB_NAMES[choice], current_or_not, address, date)

        print_flag = True

        if len(landmarks) != 0:
            landmarks_sorted = sort_landmarks(landmarks)
            for landmark in landmarks_sorted:
                print(("{} - {} градуса - {} % облачност - {} "
                       "време за път").format(
                    landmark.get_name(),
                    str(landmark.get_average_temp()),
                    str(landmark.get_cloud_percentage()),
                    str(timedelta(
                        seconds=landmark.get_travel_duration()))))

                print("Искате ли инструкции за пътуването? (1 - Да, 2 - Не)")
                instructions = '0'
                while instructions != '1' and instructions != '2':
                    instructions = input()
                    if instructions != '1' and instructions != '2':
                        print("Невалиден избор. Моля, въведете 1 или 2.")

                if instructions == '1':
                    googlish.directions_and_durations.directions(
                        landmark.get_coordinates()[0],
                        landmark.get_coordinates()[1],
                        address)

                print("Искате ли друго предложение? (1 - Да, 2 - Не)")
                is_it_okay = '0'
                while is_it_okay != '1' and is_it_okay != '2':
                    is_it_okay = input()
                    if is_it_okay != '1' and is_it_okay != '2':
                        print("Невалиден избор. Моля, въведете 1 или 2.")
                if is_it_okay == '1':
                    continue
                elif is_it_okay == '2':
                    print_flag = False
                    break
            if print_flag:
                print(
                    "Няма други места с хубаво време от избраната категория.")

        else:
            print("Няма места с хубаво време от избраната категория :(")

        print("Желаете ли да видите друга категория? (1 - Да, 2 - Не)")
        another_category = '0'
        while another_category != '1' and another_category != '2':
            another_category = input()
            if another_category != '1' and another_category != '2':
                print("Невалиден избор. Моля, въведете 1 или 2.")
        if another_category == '1':
            continue
        else:
            break
