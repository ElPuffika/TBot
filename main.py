import requests
import logging
import io
from function.yandex_maps_api import get_nearest_metro, get_route_image, get_coords
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Bot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Здравствуйте, меня зовут TBot. Я многофункциональный бот-помощник. '
                              'Выберите необходимое действие.')


def location(update, context):
    message = update.message
    current_position = (message.location.longitude, message.location.latitude)
    metro_near = get_nearest_metro(current_position[1], current_position[0])
    cord_metro = get_coords(metro_near)
    responsed = get_route_image(float(current_position[1]), float(current_position[0]), float(cord_metro[1]),
                                float(cord_metro[0]))

    update.message.reply_text(f'Ближайшая станция: {metro_near}')



def main():

    updater = Updater('5987276262:AAETidokunbdPmBFmnB7eLFYECH_FyJZBp8', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.location, location))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()