class Landmark:
    __name = None
    __closest_town = None
    __coordinates = None

    __rain_percentage = 0
    __cloud_percentage = 0
    __max_temp = 0

    def __init__(self, name, closest_town, coordinates):
        self.__name = name
        self.__closest_town = closest_town
        self.__coordinates = tuple(coordinates)

    def set_forecast_data(self, rain, cloud, max):
        self.__rain_percentage = rain
        self.__cloud_percentage = cloud
        self.__max_temp = max

    def get_name(self):
        return self.__name

    def get_closest_town(self):
        return self.__closest_town

    def get_coordinates(self):
        return self.__coordinates

    def get_rain_percentage(self):
        return self.__rain_percentage

    def get_cloud_percentage(self):
        return self.__cloud_percentage

    def get_max_temp(self):
        return self.__max_temp
