import requests


def get_nearest_metro(lat, lng):
    url = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
        "geocode": f"{lng},{lat}",
        "format": "json",
        "kind": 'metro'
    }
    response = requests.get(url, params=params)
    data = response.json()
    pos = (data["response"]["GeoObjectCollection"]["metaDataProperty"]
    ["GeocoderResponseMetaData"]["Point"]['pos']).split()
    try:
        nearest_metro = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['name']
        return nearest_metro
    except Exception:
        return 0


def get_coords(place):
    url = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": '40d1649f-0493-4b70-98ba-98533de7710b',
        "geocode": place,
        "format": "json",
    }
    response = requests.get(url, params=params)
    data = response.json()
    try:
        position = (data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]['pos']).split()
        return position
    except Exception:
        return 0


def get_route_image(lat1, lng1, lat2, lng2):
    api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
    url = "https://static-maps.yandex.ru/1.x/?"
    params = {
        "ll": f"{(lng1 + lng2) / 2},{(lat1 + lat2) / 2}",
        "size": "600,450",
        "z": "14",
        "l": "map",
        "pt": f"{lng1},{lat1},pm2rdl~{lng2},{lat2},pm2gnm",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    return response.content
