import csv
import forecast
import googlish
from landmark import Landmark

CATEGORIES = {
    '1': 'waterfalls.csv',
    '2': 'lakes.csv',
    '3': 'trails.csv',
    '4': 'peaks.csv'
}


# reads the information about the landmarks from the chosen category
# returns a list of landmarks
def read_from_csv(category):
    landmarks = []
    with open(CATEGORIES[category]) as category_file:
        reader = csv.reader(category_file, delimiter=',')
        for row in reader:
            landmarks.append(Landmark(row[0], row[1], tuple(row[2], row[3])))

    return landmarks


# uses the forecast module to extract the information about the wather
# in the landmarks from the category
def get_forecast_info(landmarks):
    pass


# gets the places in the category with nice weather and sorts
# them from best to worst
# returns a list of the reduced landmarks
def reduce_possibilities(category):
    landmarks = read_from_csv(category)
    get_forecast_info(landmarks)

    for site in landmarks:
        if site.get_rain_percentage() > 15:
            landmarks.remove(site)

    for site in landmarks:
        if site.get_cloud_percentage() > 50:
            landmarks.remove(site)

    return landmarks


def main():
    print('''Enter 1-4:
    1: Waterfalls
    2: Lakes
    3: Mountain trails
    4: Peaks''')

    while True:
        choice = input()
        if choice == '1' or choice == '2' or choice == '3' or choice == '4':
            print("You have chosen \"{}\"".format(CATEGORIES[choice]))
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            continue


if __name__ == "__main__":
    main()
