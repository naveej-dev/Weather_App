# weather_app.py

import sys
import requests
from PyQt5.QtWidgets import QApplication
from ui_weather import WeatherUI

class WeatherApp(WeatherUI):
    def __init__(self):
        super().__init__()
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "77310ca1be013761eb8a3d5c3f7de78c"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            self.display_error(f"HTTP Error: {http_error}")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Error: {req_error}")

    def display_error(self, msg):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(msg)
        self.humidity_label.clear()
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size:50px;")

        temperature_k = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        temperature_c = temperature_k - 273.15

        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.humidity_label.setText(f"{humidity}%")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌥️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())