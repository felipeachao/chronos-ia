import requests
import os

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

def get_geolocation(city):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API_KEY}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if len(data) == 0:
        return None
    
    location = data[0]
    return {
        "latitude": location.get('lat'),
        "longitude": location.get('lon'),
        "country": location.get('country')
    }

def get_weather_forecast(latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
