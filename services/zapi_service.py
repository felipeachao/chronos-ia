import requests
import os

Z_API_URL = os.getenv('Z_API_URL')
Z_API_TOKEN = os.getenv('Z_API_TOKEN')

def send_whatsapp_message(phone_number, message):
    url = f'{Z_API_URL}/send-text'
    headers = {
        'Authorization': f'Bearer {Z_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "phone": phone_number,
        "message": message
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
