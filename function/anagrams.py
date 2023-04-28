from config import BOT_TOKEN
from telegram import Bot
from telegram.ext import Filters, CommandHandler, MessageHandler, Updater
import random
import sqlite3

bot = BOT_TOKEN

global scores_full
scores_full = 0

with open('words.txt', 'r', encoding='UTF-8') as f:
    words = f.read().splitlines()

def start(update, context):
    update.message.reply_text('Игра "Анаграммы": /anagrams')

def create_anagram(word):
    shuffled_word = list(word)
    random.shuffle(shuffled_word)
    return ''.join(shuffled_word)

def anagrams(update, context):
    chat_id = update.message.chat_id
    word = random.choice(words)
    anagram = create_anagram(word)
    context.user_data['word'] = word
    context.user_data['anagram'] = anagram
    context.user_data['attempts'] = 3
    update.message.reply_text(f"Анаграмма: {anagram}. У вас есть 3 попытки.")

def guess_word(update, context):
    chat_id = update.message.chat_id
    message = update.message.text.lower()
    global scores_full
    if 'остановить игру' in message:
        update.message.reply_text("Вы остановили игру.")
        show_scores(update, context, scores_full)
        update_scores(chat_id, scores_full)
        return
    word = context.user_data['word']
    attempts = context.user_data['attempts']
    if message == word:
        scores_full += 1
        update.message.reply_text("Правильно! Следующее слово:")
        anagrams(update, context)
    else:
        attempts -= 1
        if attempts == 0:
            update.message.reply_text(f"Вы проиграли. Загаданное слово: {word}")
            show_scores(update, context, scores_full)
            update_scores(chat_id, scores_full)
        else:
            context.user_data['attempts'] = attempts
            update.message.reply_text(f"Неправильно. Осталось {attempts} попыток.")

def show_scores(update, context, scores_full):
    chat_id = update.message.chat_id
    message = f"Результаты игры: {scores_full}"
    update.message.reply_text(message)


def update_scores(chat_id, scores_full):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    select_query = f"SELECT scores FROM users WHERE id = {chat_id}"
    cursor.execute(select_query)
    current_scores = cursor.fetchone()[0]

    if current_scores == None:
        update_query = f"UPDATE users SET scores = {scores_full} WHERE id = {chat_id}"
        cursor.execute(update_query)
        conn.commit()
    elif scores_full > current_scores:
        update_query = f"UPDATE users SET scores = {scores_full} WHERE id = {chat_id}"
        cursor.execute(update_query)
        conn.commit()

    cursor.close()
    conn.close()

updater = Updater(token=bot, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('anagrams', anagrams))
dispatcher.add_handler(MessageHandler(Filters.text, guess_word))

updater.start_polling()
updater.idle()
