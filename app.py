from flask import Flask, request, jsonify
from services.openai_service import ask_openai
from services.weather_service import get_geolocation, get_weather_forecast
from services.zapi_service import send_whatsapp_message
from utils.helpers import get_today_date
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def get_weather_info():
    data = request.json
    user_question = data.get('text', {}).get('message', '')
    phone_number = data.get('phone', '')

    if not user_question or not phone_number:
        return jsonify({'error': 'Question and phone number are required!'}), 400

    today_date = get_today_date()

    gpt_analysis = ask_openai(f"""
    Identifique a cidade e a data a partir da seguinte pergunta: '{user_question}'. 
    A data de hoje é {today_date}. Ao identificar datas como 'hoje', 'amanhã', 'ontem', ou 'daqui a X dias', 
    converta essas referências temporais para datas absolutas com base na data atual fornecida ({today_date}). 
    Certifique-se de que as datas relativas sejam convertidas corretamente e retorne as datas no formato brasileiro (DD/MM/YYYY).
    Retorne a resposta em formato JSON com os campos 'City' e 'Date'.
    """)

    try:
        analysis_json = eval(gpt_analysis)
        city = analysis_json.get('City')
        date = analysis_json.get('Date')
    except (SyntaxError, ValueError):
        return jsonify({'error': 'Invalid JSON format returned by OpenAI.'}), 500

    if not city:
        return jsonify({'error': 'City not found in the response!'}), 400

    geo_info = get_geolocation(city)
    if not geo_info:
        return jsonify({'error': f'Geolocation for city {city} not found!'}), 404

    weather_data = get_weather_forecast(geo_info['latitude'], geo_info['longitude'])

    gpt_weather_response = ask_openai(f"""
    Com base nesses dados: {weather_data}, encontre a data {date} e pegue os dados relevantes sobre o clima e responda ao usuário.
    Responda de forma amigável sobre clima, umidade, vento e o que mais julgar relevante para a cidade {city}.
    """)

    send_whatsapp_message(phone_number, gpt_weather_response)

    return jsonify({'message': 'Mensagem enviada com sucesso!', 'gpt_response': gpt_weather_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000)) 
    app.run(host='0.0.0.0', port=port)