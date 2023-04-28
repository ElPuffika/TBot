import requests


def weather(coords, city):
    try:
        coordinates = coords
        url = f'https://api.weather.yandex.ru/v2/forecast?lat={coordinates[1]}&lon={coordinates[0]}'

        headers = {'X-Yandex-API-Key': '90666fa2-5763-47e1-92d7-0b7220cb2a83'}

        response = requests.get(url, headers=headers)
        data = response.json()

        city = data['geo_object']['locality']['name']
        temp = data['forecasts'][0]['parts']['day']['temp_avg']
        humidity = data['forecasts'][0]['parts']['day']['humidity']
        wind_speed = data['forecasts'][0]['parts']['day']['wind_speed']

        message = f'Погода в городе {city}:\nТемпература: {temp}°C\nВлажность: ' \
                  f'{humidity}%\nСкорость ветра: {wind_speed} м/с'
        return message
    except Exception as e:
        return ('Не удалось получить информацию о погоде в вашем регионе.\n'
                                  'Попробуйте верно ввести команду: /weather [Ваш город]')