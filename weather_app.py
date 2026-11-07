import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt   # for alignment
from PyQt5.QtGui import QFont

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")                                                                                                                               
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_name")
        self.description_label.setObjectName("description_label")

        
        self.setStyleSheet("""
               QLabel, QPushButton{
                   font-family: calibri;        
                } 
                QLabel#city_label{
                   font-size: 40px; 
                   font-style: italic;      
                }  
                QLineEdit#city_input{
                   font-size: 40px;      
                } 
                QPushButton#get_weather_button{
                   font-size: 30px;
                   font-weight: bold;       
                }          
                QLabel#temperature_label{
                   font-size: 80px;       
                }
                QLabel#emoji_label{
                   font-size: 1000px;
                   font-family: Segoe UI Emoji; 
                }
                QLabel#description_label{
                   font-size: 50px;       
                }
             """)
        
        emoji_font = QFont("Noto Color Emoji", 100)
        self.emoji_label.setFont(emoji_font)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        
        api_key = "dd84935738b60aa23af4daf662c9a812"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
        
            if data["cod"] == 200:
                self.display_weather(data)

                                              # for new name
        except requests.exceptions.HTTPError as http_error:   #Exception with status code between 400-500
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccesss is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
           self.display_error ("Timeout Error:\nThe request timeed out")
        except requests.exceptions.TooManyRedirects:
           self.display_error ("To Many Redirects:\nCheck the URL")
                                                  # for new name
        except requests.exceptions.RequestException as req_error:  #Exception due to network problems, invalid url, e.t.c
            print(f"Request Error:\n{req_error}")


    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;"
                                              "color: red;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        
    
    def display_weather(self, info):
        self.temperature_label.setStyleSheet("font-size: 80;")
        temperature_kelvin = info["main"]["temp"]
        temperature_celsius = temperature_kelvin - 273.15
        temperature_fahrenheit = (temperature_kelvin * 9/5) - 459.67
        
        weather_id = info["weather"][0]["id"]
        
        weather_description = info["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_celsius:.0f}°C/{temperature_fahrenheit:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description.title())

    @staticmethod # a static method does not depend on the instance of the class,
                  #they are used as more if a utility tool, they belong to a class but don't require any instance specific data or any other methods
    def get_weather_emoji(weather_id):
        
        # if weather_id >= 200 and weather_id <= 232: OR
        if 200 <= weather_id <= 232:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id <= 321:
            return "🌦️"  # Drizzle
        elif 500 <= weather_id <= 531:
            return "🌧️"  # Rain
        elif 600 <= weather_id <= 622:
            return "❄️"  # Snow
        elif 701 <= weather_id <= 741:
            return "🌫️"  # Atmosphere (mist, smoke, haze,dust, fog, etc.)
        elif weather_id == 762:
            return "🌋" #Volcano
        elif weather_id == 771:
            return "💨" # Squall
        elif weather_id == 781:
            return "🌪️"  # Tornado
        elif weather_id == 800:
            return "☀️"  # Clear
        elif 801 <= weather_id <= 804:
            return "☁️"  # Clouds
        else:
            return "❓"  # Unknown weather condition     


if __name__ == '__main__':  #IF WE ARE RUNNING OUR MAIN PYTHOMN FILE DIRECTLY DO THIS!!!
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())