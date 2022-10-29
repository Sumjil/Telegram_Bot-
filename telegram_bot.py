import telebot
from telebot import types
import configure
import read_file
from read_file import *
import random
import sqlite3

bot = telebot.TeleBot(configure.config['token'])
dict_todo_list = {}
st = ""
stickers_list = read_file.read("stickers.txt")
cheer_up_messages = read_file.read("messages.txt")

@bot.message_handler(commands=['start'])
def create_list(message):

    db = sqlite3.connect('tele_bot.db')
    cursor = db.cursor()

    # cursor.execute(""" CREATE TABLE Users (
    #     users_id integer ,
    #     name text
    # )""")
    # db.commit()

    # cursor.execute(""" CREATE TABLE To_do_list (
    #     task text,
    #     users_id INTEGER,
    #     FOREIGN KEY(users_id) REFERENCES Users (users_id)
    # );""")
    # db.commit()

    cursor.execute(f"SELECT users_id FROM Users WHERE users_id = {message.chat.id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f'INSERT INTO Users VALUES ({message.chat.id}, "{message.chat.first_name}");')
        db.commit()
    # else:
    #     bot.send_message(message.from_user.id, "You are in the database")

    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Add tasks to the to-do list"))
    rmk.add(types.KeyboardButton("Show me my to-do list"))
    rmk.add(types.KeyboardButton("Done some of the task"))
    msg = bot.send_message(message.chat.id,
                           "Hi, using this bot you can add tasks to to-do list\nlet's start click on button 'Add tasks to the to-do list' ",
                           reply_markup=rmk)
    bot.register_next_step_handler(msg, user_answer)

# @bot.message_handler(commands=['delete'])
# def delete (message):
#     db = sqlite3.connect('tele_bot.db')
#     cursor = db.cursor()
#     people_id = message.chat.id
#     cursor.execute(f"DELETE FROM To_do_list")
#     db.commit()
#     bot.send_message(message.from_user.id, "delete")


@bot.message_handler(content_types=['text'])
def user_answer(message):
    global st
    db = sqlite3.connect('tele_bot.db')
    cursor = db.cursor()
    if message.text == "Add tasks to the to-do list":
        bot.send_message(message.from_user.id,
                         "Start adding your tasks and when you finish send me a dot .")
        bot.register_next_step_handler(message, get_task)
    elif message.text == "Show me my to-do list":
        bot.send_message(message.from_user.id, f"Your to-do list:\n{write_todo_list(message)}")
    elif message.text == "Done some of the task":
        bot.send_message(message.from_user.id,
                         "Choose the index number of the task you have done when you finish send me a dot .")
        bot.register_next_step_handler(message, done_task)

    else:
        bot.send_message(message.from_user.id, "I can't understand you :(")


def get_task(message):
    db = sqlite3.connect('tele_bot.db')
    cursor = db.cursor()
    text_from_user = message.text
    if message.text is not None:
        if text_from_user != '.':
            cursor.execute(f'INSERT INTO To_do_list VALUES ( "{text_from_user}", {message.chat.id});')
            db.commit()
            bot.send_message(message.from_user.id, 'Added')
            bot.register_next_step_handler(message, get_task)
        else:
            bot.send_message(message.from_user.id, f"Your to-do list:\n{write_todo_list(message)}")
    else:
        bot.send_message(message.from_user.id, "I can read only text. Try again")
        bot.register_next_step_handler(message, get_task)


def done_task(message):
    global st
    text_from_user = message.text
    db = sqlite3.connect('tele_bot.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT task FROM To_do_list WHERE users_id = {message.from_user.id} ")
    all_tasks = cursor.fetchall()
    db.commit()
    if message.text is not None:
        if text_from_user.isdigit() and int(text_from_user) <= len(all_tasks) and int(text_from_user) > 0:
            cursor.execute(f'DELETE FROM To_do_list WHERE task = "{all_tasks[int(text_from_user)-1][0]}";')
            db.commit()
            bot.send_sticker(message.chat.id, sticker=random.choice(stickers_list))
            bot.send_message(message.from_user.id, random.choice(cheer_up_messages))
            bot.send_message(message.from_user.id, f"Your to-do list:\n{write_todo_list(message)}")
            bot.register_next_step_handler(message, done_task)
        elif text_from_user == '.':
            bot.send_message(message.from_user.id, f"Your to-do list:\n{write_todo_list(message)}")
        else:
            bot.send_message(message.from_user.id,
                             f"You sent something incorrectly, maybe the wrong number of your task or your to-do list is empty\n Try again or send me a dot . to exit to the main menu")
            bot.register_next_step_handler(message, done_task)
    else:
        bot.send_message(message.from_user.id, "I can read only text. Try again")
        bot.register_next_step_handler(message, done_task)


def write_todo_list(message):
    db = sqlite3.connect('tele_bot.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT task FROM To_do_list WHERE users_id = {message.chat.id} ")
    all_tasks = cursor.fetchall()
    db.commit()
    st = ""
    for i in range(0, len(all_tasks)):
        st += f"🗃 {i + 1}. {all_tasks[i][0]}\n"
    return st


bot.polling(none_stop=True, interval=0)
