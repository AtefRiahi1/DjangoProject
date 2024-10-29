import requests
from datetime import datetime

WEATHER_API_KEY = '5465bc7d107d41f9a01162729242510'  # Replace with your WeatherAPI key
GEOCODE_API_KEY = 'ce9cf096220d40458d0e3b2502573bf0'  # Replace with your OpenCage API key
BASE_WEATHER_URL = 'http://api.weatherapi.com/v1/forecast.json'
BASE_GEOCODE_URL = 'https://api.opencagedata.com/geocode/v1/json'

# Global variable to hold the weather dataset
weather_dataset = {}

def get_coordinates(zone):
    # Use OpenCage Geocoding API to retrieve coordinates for any location
    response = requests.get(f"{BASE_GEOCODE_URL}?q={zone}&key={GEOCODE_API_KEY}")
    data = response.json()

    if response.status_code == 200 and data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        print("Location not found. Please enter a valid location.")
        return None, None

def fetch_weather_data(zone):
    lat, lon = get_coordinates(zone)

    if lat is None or lon is None:
        return

    # Make a request to the WeatherAPI
    response = requests.get(f"{BASE_WEATHER_URL}?q={lat},{lon}&days=5&key={WEATHER_API_KEY}&aqi=no&alerts=no")
    
    if response.status_code != 200:
        print("Failed to retrieve weather data.")
        return

    data = response.json()

    # Store the data in the dataset
    weather_data = []
    for day in data['forecast']['forecastday']:
        weather_data.append({
            "date": day['date'],
            "temperature": day['day']['avgtemp_c'],
            "humidity": day['day']['avghumidity'],
            "precipitation": day['day']['totalprecip_mm'],
            "wind_speed": day['day']['maxwind_kph'],
        })

    # Save it to the global dataset
    weather_dataset[zone] = weather_data
    print("Weather data saved successfully.")

def best_day_for_irrigation(zone):
    weather_data = weather_dataset.get(zone)

    if not weather_data:
        print("No weather data available for this zone.")
        return

    # Display the 5-day forecast
    print("\n5-Day Weather Forecast:")
    for weather in weather_data:
        print(f"Date: {weather['date']}, Temp: {weather['temperature']}°C, Humidity: {weather['humidity']}%, Precipitation: {weather['precipitation']} mm, Wind Speed: {weather['wind_speed']} kph")

    # Exclude today's date
    today = datetime.now().date()

    # Find the best day for irrigation, skipping today
    best_day = None
    for weather in weather_data:
        forecast_date = datetime.strptime(weather['date'], "%Y-%m-%d").date()
        if forecast_date <= today:
            continue  # Skip today's date

        # Check if this day meets the irrigation criteria and is better than any previous day
        if best_day is None or (
            weather['precipitation'] == 0 and 15 < weather['temperature'] < 30
        ):
            best_day = weather

    # Output the best day if found
    if best_day:
        print("\nBest day for irrigation:")
        print(f"Date: {best_day['date']}")
        print(f"Temperature: {best_day['temperature']}°C")
        print(f"Humidity: {best_day['humidity']}%")
        print(f"Precipitation: {best_day['precipitation']} mm")
        print(f"Wind Speed: {best_day['wind_speed']} kph")
        
        # Explanation
        print("\nReasoning:")
        print("This day is suitable for irrigation because:")
        if best_day['precipitation'] == 0:
            print("- No precipitation, meaning there won't be excess water from rain.")
        if 15 < best_day['temperature'] < 30:
            print(f"- Temperature is within the ideal range for irrigation ({best_day['temperature']}°C).")
        if best_day['wind_speed'] < 20:
            print(f"- Wind speed is manageable ({best_day['wind_speed']} kph), reducing the risk of water drift.")
    else:
        print("No suitable day found for irrigation.")

if __name__ == "__main__":
    zone = input("Please enter a location (city or place name): ")
    fetch_weather_data(zone)
    best_day_for_irrigation(zone)
