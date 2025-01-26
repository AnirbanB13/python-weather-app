import datetime
import requests
import string
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
OWM_FORECAST_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
GEOCODING_API_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
api_key = os.getenv("OWM_API_KEY")

app = Flask(__name__)


# Display home page and get city name entered into the search form
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form.get("search")
        return redirect(url_for("get_weather", city=city))
    return render_template("index.html")


# Display weather forecast for a specific city using data from OpenWeather API
@app.route("/<city>", methods=["GET", "POST"])
def get_weather(city):
    city_name = string.capwords(city)
    today = datetime.datetime.now()
    current_date = today.strftime("%A, %B %d")

    location_params = {
        "q": city_name,
        "appid": api_key,
        "limit": 3,
    }

    try:
        # Fetch city coordinates
        location_response = requests.get(GEOCODING_API_ENDPOINT, params=location_params)
        location_response.raise_for_status()
        location_data = location_response.json()
        print("Location Response:", location_data)

        if not location_data:
            return redirect(url_for("error"))

        lat = location_data[0].get("lat")
        lon = location_data[0].get("lon")
        if not lat or not lon:
            return redirect(url_for("error"))

        # Fetch weather data
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
        }
        weather_response = requests.get(OWM_ENDPOINT, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        print("Weather Response:", weather_data)

        current_temp = round(weather_data["main"]["temp"])
        current_weather = weather_data["weather"][0]["main"]
        min_temp = round(weather_data["main"]["temp_min"])
        max_temp = round(weather_data["main"]["temp_max"])
        wind_speed = weather_data["wind"]["speed"]

        # Fetch five-day weather forecast
        forecast_response = requests.get(OWM_FORECAST_ENDPOINT, params=weather_params)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        five_day_temp_list = [
            round(item["main"]["temp"]) for item in forecast_data["list"] if "12:00:00" in item["dt_txt"]
        ]
        five_day_weather_list = [
            item["weather"][0]["main"] for item in forecast_data["list"] if "12:00:00" in item["dt_txt"]
        ]
        five_day_unformatted = [
            today,
            today + datetime.timedelta(days=1),
            today + datetime.timedelta(days=2),
            today + datetime.timedelta(days=3),
            today + datetime.timedelta(days=4),
        ]
        five_day_dates_list = [date.strftime("%a") for date in five_day_unformatted]

        return render_template(
            "city.html",
            city_name=city_name,
            current_date=current_date,
            current_temp=current_temp,
            current_weather=current_weather,
            min_temp=min_temp,
            max_temp=max_temp,
            wind_speed=wind_speed,
            five_day_temp_list=five_day_temp_list,
            five_day_weather_list=five_day_weather_list,
            five_day_dates_list=five_day_dates_list,
        )

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return redirect(url_for("error"))
    except KeyError as e:
        print(f"KeyError: {e}")
        return redirect(url_for("error"))


# Display error page for invalid input or issues with the API
@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__
    # Run the app on all interfaces
    app.run(debug=True, host="0.0.0.0")
