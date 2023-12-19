import requests
import telebot
from telebot import types

bot = telebot.TeleBot('API_TOKEN')


@bot.message_handler(commands=['start'])
def greeting(message):
    if message.from_user.last_name == None:
        user_name = message.from_user.first_name
    elif message.from_user.last_name != None:
        user_name = message.from_user.first_name + message.from_user.last_name

    global greetings_text
    greetings_text = f'''Hello, <b>{
        user_name}</b>! 👋\nI'm a telegram-bot created to generate castom password.\nTo start the generation process use the command: "/weather".'''

    bot.send_message(message.chat.id, greetings_text, parse_mode='HTML')


@bot.message_handler(commands=['weather'])
def choose_city(message):
    bot.send_message(
        message.chat.id, 'Please, write the name of the city whose weather you are interested in:', parse_mode='HTML')
    bot.register_next_step_handler(message, show_weather)


def show_weather(message):
    city = str(message.text.strip())
    api_key = 'API_KEY'
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + \
        '&units=metric&lang=ru&appid=' + api_key
    weather_data = requests.get(url).json()

    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    weather = weather_data['weather'][0]['main']
    wind = round(weather_data['wind']['speed'])
    humidity = weather_data['main']['humidity']
    pressure = round(weather_data['main']['pressure']/1.33)

    bot.send_message(message.chat.id, f'''
                     Now in city {city}\n🌡️: {temperature}°C (it feels like  {temperature_feels}°C)\n⛅: {weather}\n💨: {wind} m/s\n💦: {humidity} %\n⚠️: {pressure} m. of m.\n\nTo know the weather of another city use command: "/weather".
                     ''')


bot.polling(none_stop=True)
