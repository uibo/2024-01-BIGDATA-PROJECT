import requests
import json

apikey = "daf764df314a58e005edce3b73c6af22"


cities = ["Seoul", "Tokyo", "New York"]

api = "https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}"


k2c = lambda k: k - 273.15

for city in cities:
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}")
    data = json.loads(response.text)

    print("+ City = " + str(data["name"]))
    print("| WEATHER = " + str(data["weather"][0]["description"]))
    print("| MAX_TEMP = " + str(k2c(data["main"]["temp_max"])))
    print("| MIN_TEMP = " + str(k2c(data["main"]["temp_min"])))
    print("| HUMIDITY = " + str(data["main"]["humidity"]))
    print("| PRESSURE = " + str(data["main"]["pressure"]))
    print("| DEG = " + str(data["wind"]["deg"]))
    print("| SPEED = " + str(data["wind"]["speed"]))