import requests
from flask import Flask, render_template, request 

app = Flask(__name__)
api_key = "59591df3f4e37c03b5d4b9a7942434c6"


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data['main']['temp'],
            "condition": data['weather'][0]['description'],
            "wind_speed": data['wind']['speed'],
            "humidity": data['main']['humidity'],
            "icon": data['weather'][0]['icon'],
            "name": city
        }
    else:
        return {"error": "City not found"}


@app.route('/', methods=['POST', 'GET'])
def index():
    weather_data = None
    city_list = ["Pune", "Chennai", "Mumbai", "Kolkata"]
    cities_weather = {}

    # Get data for each city
    for city in city_list:
        cities_weather[city] = get_weather(city)

    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)

    return render_template('index.html', weather_data=weather_data, cities_weather=cities_weather)


if __name__ == "__main__":
    app.run(debug=True)
