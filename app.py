from flask import Flask, request, jsonify
from services.openai_service import ask_openai
from services.weather_service import get_geolocation, get_weather_forecast, handle_weather_query
from services.zapi_service import send_whatsapp_message
from utils.detect_intent import detect_intent
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data.get('text', {}).get('message', '')
    phone_number = data.get('phone', '')

    if not user_message or not phone_number:
        return jsonify({'error': 'Message and phone number are required!'}), 400

    intent = detect_intent(user_message)
    
    if intent == "weather":
        response_message = handle_weather_query(user_message)
    else:
        response_message = ask_openai(user_message)

    send_whatsapp_message(phone_number, response_message)

    return jsonify({'status': 'success', 'message': 'Resposta enviada via WhatsApp', 'response': response_message})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
