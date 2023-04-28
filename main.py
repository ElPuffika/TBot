import logging
import sqlite3
from telegram import ReplyKeyboardMarkup, KeyboardButton
from function.yandex_maps_api import get_nearest_metro, get_route_image, get_coords
from function.yandex_weather_api import weather
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

button_start = KeyboardButton('/start')

keyboard = [[button_start]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def start(update, context):
    conn = sqlite3.connect('function/users.db')
    cursor = conn.cursor()

    user_id = update.effective_user.id
    user_fname = update.effective_user.first_name

    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    result = cursor.fetchone()

    texth = f"Привет, {user_fname}! меня зовут TBot. Я многофункциональный бот-помощник." \
            f"Выберите необходимое действие.\n\n" \
            f"— Ближайшее метро: /location.\n" \
            f"— Погода: /weather [город]."

    if result:
        if result[1] != user_fname:
            context.bot.send_message(chat_id=user_id, text=texth)
            context.bot.send_message(chat_id=user_id, text=f"Вы изменили имя вашего профиля с {result[1]} "
                                                           f"на {user_fname}. Изменения внесены в базу данных.")
            conn.commit()
            cursor.execute('UPDATE users SET username = ? AND scores = ? WHERE id = ?', (user_fname, 0, user_id))
            conn.commit()
        else:
            context.bot.send_message(chat_id=user_id, text=texth)
    else:
        context.user_data['id'] = user_id
        context.user_data['username'] = user_fname

        cursor.execute(f"INSERT INTO users VALUES ({user_id}, '{user_fname}', 0)")
        conn.commit()

        context.bot.send_message(chat_id=user_id, text=texth)


def menu(update, context):
    update.message.reply_text(text=f'Вы находитесь в меню.'
                                   f"Выберите необходимое действие.\n\n"
                                   f"— Ближайшее метро: /location.\n"
                                   f"— Погода в вашем регионе: /weather [город].")


def location(update, context):
    button = KeyboardButton(text="Отправить местоположение", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text="Пожалуйста, отправьте свое местоположение", reply_markup=reply_markup)

def get_location(update, context):
    message = update.message
    current_position = (message.location.longitude, message.location.latitude)
    id_chat = message.chat.id
    metro_near = get_nearest_metro(current_position[1], current_position[0])
    cord_metro = get_coords(metro_near)
    try:
        responsed = get_route_image(float(current_position[1]), float(current_position[0]), float(cord_metro[1]),
                                    float(cord_metro[0]))
        update.message.reply_text(f'Ближайшая станция: {metro_near}')
        context.bot.send_photo(chat_id=id_chat, photo=responsed)
        update.message.reply_text('Для повторного запроса отправьте свою геопозицию еще раз.'
                                  ' Чтобы вернуться обратно: /menu')
    except Exception as e:
        update.message.reply_text('Рядом с вами метро не найдено. Попробуйте указать другую геопозицию.')


def get_weather(update, context):
    try:
        message = update.message
        coords = get_coords((message['text'].replace('/weather ', '')))
        if coords == 0:
            update.message.reply_text('Не удалось получить информацию о погоде.\n'
                                  'Попробуйте верно ввести команду: /weather [Ваш город]')
        else:
            update.message.reply_text(weather(coords, (message['text'].replace('/weather ', ''))))
    except Exception as e:
        update.message.reply_text('Не удалось получить информацию о погоде в вашем регионе.\n'
                                  'Попробуйте верно ввести команду: /weather [Ваш город]')


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    menu_handler = CommandHandler('menu', menu)
    dispatcher.add_handler(menu_handler)

    location_handler = CommandHandler('location', location)
    dispatcher.add_handler(location_handler)

    dispatcher.add_handler(MessageHandler(Filters.location, get_location))

    weather_handler = CommandHandler('weather', get_weather)
    dispatcher.add_handler(weather_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
