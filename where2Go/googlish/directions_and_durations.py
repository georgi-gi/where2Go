import requests

GOOGLE_API_KEY = "AIzaSyC79GdoRDJXfeWDQnx5bBr14I3HJgEBIH0"


def get_current_coordinates():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    return (data['lat'], data['lon'])


def tranform_html_directions(data):
    # transform to text or put into json
    for step in data['routes'][0]['legs'][0]['steps']:
        step['html_instructions']


def get_duration(destination_lat, destination_lon):
    current_position = get_current_coordinates()

    url = "https://maps.googleapis.com/maps/api/directions/json?origin={},{}&destination={},{}&key={}&language=bg&traffic_model".format(
        current_position[0], current_position[1],
        destination_lat, destination_lon, GOOGLE_API_KEY)

    response = requests.get(url)
    data = response.json()
    return data['routes'][0]['legs'][0]['duration']['value']


def directions(destination_lat, destination_lon):
    current_position = get_current_coordinates()

    url = "https://maps.googleapis.com/maps/api/directions/json?origin={},{}&destination={},{}&key={}&language=bg".format(
        current_position[0], current_position[1],
        destination_lat, destination_lon, GOOGLE_API_KEY)

    response = requests.get(url)

    data = response.json()
    tranform_html_directions(data)
