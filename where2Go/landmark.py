class Landmark:
    __name = None
    __lat = 0
    __lon = 0
    __travel_duration = 0

    __cloud_percentage = 0
    __average_temp = 0

    def __init__(self, name, lat, lon):
        self.__name = name
        self.__lat = lat
        self.__lon = lon

    def set_forecast_data(self, cloud, average):
        self.__cloud_percentage = cloud
        self.__average_temp = average

    def set_travel_duration(self, duration):
        self.__travel_duration = duration

    def get_travel_duration(self):
        return self.__travel_duration

    def get_name(self):
        return self.__name

    def get_coordinates(self):
        return (self.__lat, self.__lon)

    def get_cloud_percentage(self):
        return self.__cloud_percentage

    def get_average_temp(self):
        return self.__average_temp
