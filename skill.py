from datetime import datetime
from astral.sun import sun
from astral import location
import logging

# Инициализируем логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_sun_position(user_latitude, user_longitude):
    city = location(('user_location', 'user_region', user_latitude, user_longitude, 'UTC'))
    s = sun(city.observer, date=datetime.now())
    return s.altitude, s.azimuth

def get_response(user_latitude, user_longitude):
    altitude, azimuth = get_sun_position(user_latitude, user_longitude)
    return f"Солнце находится на высоте {altitude:.2f} градусов и имеет азимут {azimuth:.2f} градусов от севера."

def handle_dialog(request, response):
    # Получаем координаты пользователя
    user_location = request.get_coordinates('google')['response']['geo_object']['point']['pos']
    user_latitude, user_longitude = map(float, user_location.split())

    # Получаем ответ с положением Солнца
    sun_position = get_response(user_latitude, user_longitude)

    # Формируем и отправляем ответ пользователю
    response.set_text(sun_position)
    response.set_end_session(True)
