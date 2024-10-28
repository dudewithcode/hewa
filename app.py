from flask import Flask, request, render_template
from utils.utils import get_weather_data, get_location, get_current, week_forecast, today_forecast
from flask_redis import FlaskRedis

app = Flask(__name__)


# Configure Redis
app.config['REDIS_URL'] = "redis://localhost:6379/0"
redis_client = FlaskRedis(app)


@app.route('/', methods=['GET'])
def home():
    city = request.args.get('city', '').strip() or 'Nairobi'
    weather_data = get_weather_data(city)
    location = get_location(weather_data)
    current_weather = get_current(weather_data)
    week_weather = week_forecast(weather_data)
    today_weather = today_forecast(weather_data)

    return render_template('index.html', location=location, current=current_weather, today=today_weather, week=week_weather)

@app.route('/see-more', methods=['GET'])
def see_more():
    city = request.args.get('city', '').strip() or 'Nairobi'
    weather_data = get_weather_data(city)
    
    if weather_data:
        # Gather more detailed data for the forecast
        location = get_location(weather_data)
        current_weather = get_current(weather_data)
        week_weather = week_forecast(weather_data)
        today_weather = today_forecast(weather_data)

        # Render the detailed forecast template
        return render_template('base.html', location=location, current=current_weather, today=today_weather, week=week_weather)
    else:
        error_message = f"Could not retrieve weather data for {city}. Please try another city."
        return render_template('base.html', error=error_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)