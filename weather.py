import requests
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city="Tashkent"):
    """Получает текущую погоду для указанного города."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"].capitalize()
            return temp, description, city
        else:
            return None, "⚠️ Не удалось получить погоду. Проверьте API-ключ или название города.", None
    except Exception as e:
        return None, f"⚠️ Ошибка при получении погоды: {str(e)}", None