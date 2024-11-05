import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from flask import render_template

# Load environment variables from the .env file
load_dotenv()

# Retrieve variables from environment
API_KEY = os.getenv('API_KEY')
CACHE_EXPIRATION = int(os.getenv('CACHE_EXPIRATION', 3600))

def get_weather_data_from_api(city, days=7):
    url = 'https://api.weatherapi.com/v1/forecast.json?q={}&days={}&aqi=no&key={}'.format(city, days, API_KEY)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for HTTP errors (e.g., 404)
        return response.json()       # Return the JSON data if successful
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None  # Return None if any error occurs

def get_cached_weather_data(city):
    """
    Fetch weather data for the given city from Redis cache if available.
    If not, fetch from external API and store in Redis.
    """

    from app import redis_client
    cache_key = f"weather:{city.lower()}"  # Use a standardized key format
    try:
        # Check if the weather data is already cached
        weather_data = redis_client.get(cache_key)
        if weather_data:
            # Store fetched data in Redis with an expiration
            redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(weather_data))
            return weather_data
        else:
            return None
    except Exception as e:
        # In case Redis is down or any other issue, log the error and fetch directly from the API
        print(f"Redis error: {e}. Fetching data directly from the API...")
        return get_weather_data_from_api(city)

def get_weather_data(city):
    return get_cached_weather_data(city)

def get_location(data):

    return data['location']

def get_current(data):

    return data['current']

def week_forecast(data):
    forecast_days = data['forecast']['forecastday']
    l = []
    for obj in forecast_days:
        d = {}
        date = datetime.strptime(obj['date'], '%Y-%m-%d')
        today = datetime.now()
        if date.date() == today.date():
            result = "Today"
        else:
            result = date.strftime('%A')
        d['day'] = result
        d['maxtemp_c'] = round(obj['day']['maxtemp_c'])
        d['maxtemp_f'] = round(obj['day']['maxtemp_c'])
        d['mintemp_c'] = round(obj['day']['mintemp_c'])
        d['mintemp_f'] = round(obj['day']['mintemp_f'])
        d['text'] = obj['day']['condition']['text']
        d['icon'] = obj['day']['condition']['icon']
        l.append(d)
    return l

def today_forecast(data):
    time = [6, 9, 12, 15, 18, 21]
    l = []
    for t in time:
        today = data['forecast']['forecastday'][0]['hour'][t]
        d = {}
        d['chance_of_rain'] = data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
        dt = datetime.strptime(today['time'], '%Y-%m-%d %H:%M')
        time_12hr = dt.strftime('%I:%M %p')
        d['time'] = time_12hr
        d['icon'] = today['condition']['icon']
        d['temp_c'] = round(today['temp_c'])
        d['temp_f'] = round(today['temp_f'])
        l.append(d)
    return l


def fetch_weather_data(city):
    """Fetches and returns weather data or defaults to Nairobi if no data."""
    weather_data = get_weather_data(city)
    if not weather_data:  # Default to Nairobi if no data found for city
        city = 'Nairobi'
        weather_data = get_weather_data(city)
    return {
        "location": get_location(weather_data),
        "current": get_current(weather_data),
        "today": today_forecast(weather_data),
        "week": week_forecast(weather_data),
        "city": city
    }


def render_weather_template(template_name, weather_data, error=None):
    """Renders the template with the weather data and optional error message."""
    return render_template(
        template_name,
        location=weather_data["location"],
        current=weather_data["current"],
        today=weather_data["today"],
        week=weather_data["week"],
        error=error
    )