import os
import requests
from utils.helpers import get_today_date
from services.openai_service import ask_openai

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

def get_geolocation(city):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={WEATHER_API_KEY}'
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

def handle_weather_query(user_message):

    today_date = get_today_date()

    gpt_analysis = ask_openai(f"""
    Identifique a cidade e a data a partir da seguinte pergunta: '{user_message}'. 
    A data de hoje é {today_date}. Ao identificar datas como 'hoje', 'amanhã', 'ontem', ou 'daqui a X dias', 
    converta essas referências temporais para datas absolutas com base na data atual fornecida ({today_date}). 
    Certifique-se de que as datas relativas sejam convertidas corretamente e retorne as datas no formato brasileiro (DD/MM/YYYY).
    Retorne a resposta em formato JSON com os campos 'City' e 'Date'.
    """)
        
    
    try:
        analysis_json = eval(gpt_analysis)
        city = analysis_json.get('City')
    except:
        return "Desculpe, não consegui identificar a cidade."

    if not city:
        return "Desculpe, não consegui identificar a cidade."
    
    date = analysis_json.get('Date')

    geo_info = get_geolocation(city)
    if not geo_info:
        return f"Não consegui encontrar informações de localização para a cidade {city}."

    weather_data = get_weather_forecast(geo_info['latitude'], geo_info['longitude'])
    return ask_openai(f"Com base nesses dados: {weather_data}, responda sobre a previsão do clima para {city} e para o dia {date}.")
