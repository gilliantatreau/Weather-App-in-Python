# Author Gillian Tatreau
# Date Created 13 August 2022
import requests
import config


def main():
    """calls functions, repeats forecast lookup"""
    print("welcome to the weather forecast generator")
    try:
        call_functions()
    except IndexError:  # catches any errors in the city lookup
        print("there has been an error please try again")
    while True:
        repeat = input("would you like to look up another location's weather forecast? y/n\n")
        if repeat.lower() == "y":
            call_functions()
        elif repeat.lower() == "n":
            print("good bye")
            break
        else:
            print("please enter y to look up another location's weather forecast and n to exit")


def call_functions():
    """asks for user input for how to lookup weather forecasts, validates inputs, calls functions"""
    while True:
        city_or_zip = input("how would you like to search for the weather forecast? "
                            "please enter 1 for us city name or 2 for us zip code: ")
        if int(city_or_zip) == 1:
            break
        elif int(city_or_zip) == 2:
            break
        else:
            print("please enter 1 for city name or 2 for zip code")
    while True:
        temp_unit = input("what unit of measurement do you want to read the weather forecast? "
                          "f for Fahrenheit, c for Celsius, k for Kelvin\n")
        if temp_unit.lower() == "f":
            break
        elif temp_unit.lower() == "c":
            break
        elif temp_unit.lower() == "k":
            break
        else:
            print("please enter f for fahrenheit, c for celsius, and k for kelvin")
    try:
        coordinates = get_lat_lon(city_or_zip)
        latitude = coordinates[0]
        longitude = coordinates[1]
        weather_forecast(temp_unit, latitude, longitude)
    except (TypeError, IndexError):     # error handling for zip lookup
        print("there has been an error please try again")


def get_lat_lon(city_or_zip):
    """queries API for latitude and longitude for city lookup and zip lookup methods"""
    if int(city_or_zip) == 1:
        city = input("please enter a city name: ")
        state = input("please enter a state abbreviation: ")
        response = requests.request("GET", f"http://api.openweathermap.org/geo/1.0/direct?"
                                           f"q={city.lower()},{state.lower()},us&appid={config.api_key}")
        print("\ncurrent weather conditions for: ", city)
    elif int(city_or_zip) == 2:
        place = input("please enter the zip code: ")
        try:
            response = requests.request("GET", f"http://api.openweathermap.org/geo/1.0/zip?zip={place},us"
                                               f"&appid={config.api_key}")
        except UnboundLocalError:   # error handling for zip lookup
            print("there has been an error please try again")
        print("\ncurrent weather conditions for zip code: ", place)
    else:
        print("please enter 1 for city name or 2 for zip code")
    if response.status_code == 200 and int(city_or_zip) == 1:
        city_data = response.json()
        lat = city_data[0]["lat"]
        lon = city_data[0]["lon"]
    elif response.status_code == 200 and int(city_or_zip) == 2:
        zip_data = response.json()
        lat = zip_data["lat"]
        lon = zip_data["lon"]
    else:
        print(response.status_code)
        print("an error has occurred please try again")
    try:
        return lat, lon
    except (IndexError, UnboundLocalError):     # error handling for zip lookup
        print("there has been an error please try again")


def weather_forecast(temp_unit, latitude, longitude):
    """queries API for weather forecast, given latitude and longitude"""
    if temp_unit.lower() == "f":
        unit = "imperial"
    elif temp_unit.lower() == "c":
        unit = "metric"
    else:
        unit = "standard"
    forecast = requests.request("GET",
                                f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}"
                                f"&appid={config.api_key}&units={unit}")
    if forecast.status_code == 200:
        weather_data = forecast.json()
        pretty_print(weather_data)
    else:
        print(forecast.status_code)
        print("an error has occurred please try again")


def pretty_print(weather_data):
    """parses JSON from API query and formats/prints weather information nicely"""
    print("current temperature: ", weather_data["list"][0]["main"]["temp"], " degrees")
    print("high temp: ", weather_data["list"][0]["main"]["temp_max"], " degrees")
    print("low temp: ", weather_data["list"][0]["main"]["temp_min"], " degrees")
    print("pressure: ", weather_data["list"][0]["main"]["pressure"], " hPa")
    print("humidity: ", weather_data["list"][0]["main"]["humidity"], " %")
    print("cloud cover: ", weather_data["list"][0]["weather"][0]["main"])
    print("description: ", weather_data["list"][0]["weather"][0]["description"], "\n")


if __name__ == "__main__":
    main()
