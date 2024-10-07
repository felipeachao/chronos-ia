def detect_intent(user_message):
    weather_keywords = ["previsão do tempo", "clima", "temperatura", "chuva", "sol", "vai chover", "como está o tempo"]
    if any(word in user_message.lower() for word in weather_keywords):
        return "weather"
    return "general"
