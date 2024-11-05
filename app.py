from flask import Flask, request
from utils.utils import fetch_weather_data, render_weather_template
from flask_redis import FlaskRedis

# Initialize Flask application
app = Flask(__name__)

# Configure Redis for caching
# Redis URL should point to the Redis server; in this case, it's local.
app.config['REDIS_URL'] = "redis://localhost:6379/0"
redis_client = FlaskRedis(app)  # Initialize Redis client

# Route for the home page
@app.route('/', methods=['GET'])
def home():
    """
    Renders the homepage displaying weather data for a specified city.
    
    Parameters:
    - city: str (optional) - City name provided by the user through query parameters.
             Defaults to 'Nairobi' if not specified.

    Workflow:
    1. Retrieves the city name from query parameters (or defaults to Nairobi).
    2. Fetches weather data using fetch_weather_data function.
    3. Checks if the data is valid (matches the requested city).
    4. Returns the rendered HTML template with the weather data.
       If there's an error (e.g., city not found), displays an error message
       and shows results for Nairobi.

    Returns:
    - Rendered HTML template displaying the weather data for the city.
    """
    city = request.args.get('city', '').strip() or 'Nairobi'  # Retrieve or default to 'Nairobi'
    weather_data = fetch_weather_data(city)  # Get weather data for the specified city
    
    # Check if weather data retrieval was successful
    if weather_data["city"] != city:
        error_message = f"Could not retrieve weather data for '{city}'. Showing results for Nairobi."
        return render_weather_template('index.html', weather_data, error=error_message)
    
    # Render the homepage with the fetched weather data
    return render_weather_template('index.html', weather_data)


# Route for the 'See More' page
@app.route('/see-more', methods=['GET'])
def see_more():
    """
    Renders a more detailed weather information page for a specified city.

    Parameters:
    - city: str (optional) - City name provided by the user through query parameters.
             Defaults to 'Nairobi' if not specified.

    Workflow:
    1. Retrieves the city name from query parameters (or defaults to Nairobi).
    2. Fetches weather data using fetch_weather_data function.
    3. Checks if the data is valid (matches the requested city).
    4. Returns the rendered HTML template with the weather data.
       If there's an error (e.g., city not found), displays an error message
       and shows results for Nairobi.

    Returns:
    - Rendered HTML template with detailed weather information for the city.
    """
    city = request.args.get('city', '').strip() or 'Nairobi'  # Retrieve or default to 'Nairobi'
    weather_data = fetch_weather_data(city)  # Get weather data for the specified city
    
    # Check if weather data retrieval was successful
    if weather_data["city"] != city:
        error_message = f"Could not retrieve weather data for {city}. Showing results for Nairobi."
        return render_weather_template('base.html', weather_data, error=error_message)
    
    # Render the detailed page with the fetched weather data
    return render_weather_template('base.html', weather_data)


# Entry point for running the application
if __name__ == "__main__":
    # Run the application on host 0.0.0.0 at port 5000 with debugging enabled
    app.run(host="0.0.0.0", port=5000, debug=True)
