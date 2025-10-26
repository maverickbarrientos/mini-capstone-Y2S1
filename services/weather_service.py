import requests, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_forecast(lat, lon):
    source = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"

    response = requests.get(source)
    data = response.json()

    time_now = datetime.now()

    weather_forecast = [forecast for forecast in data["list"] if datetime.strptime(forecast['dt_txt'], "%Y-%m-%d %H:%M:%S") > time_now]
    return weather_forecast[2] or []

def get_latest_forecast(lat, lon):
    source = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"

    response = requests.get(source)
    data = response.json()
    
    time_now = datetime.now()

    weather_forecast = [forecast for forecast in data["list"] if datetime.strptime(forecast['dt_txt'], "%Y-%m-%d %H:%M:%S") > time_now]
    return weather_forecast[0] or []