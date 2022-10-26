import telebot
from telebot import types
import configure
import read_file
from read_file import *
import random

bot = telebot.TeleBot(configure.config['token'])
to_do_list =[]
st = ""
stickers_list = read_file.read("stickers.txt")
cheer_up_messages = read_file.read("messages.txt")

@bot.message_handler(commands=['start'])
def create_list(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Add tasks to the to-do list"))
    rmk.add(types.KeyboardButton("Show me my to-do list"))
    rmk.add(types.KeyboardButton("Done some of the task"))
    msg = bot.send_message(message.chat.id,  "Hi, using this bot you can add tasks to to-do list\nlet's start click on button 'Add tasks to the to-do list' ", reply_markup= rmk)
    bot.register_next_step_handler(msg, user_answer)

@bot.message_handler(content_types=['text'])
def user_answer(message):

    if message.text == "Add tasks to the to-do list":
        bot.send_message(message.from_user.id,
                         "Start adding your tasks and when you finish send me a dot .")
        bot.register_next_step_handler(message, get_task)
    elif message.text == "Show me my to-do list":
        bot.send_message(message.from_user.id, f"Your to-do list:\n{st}")
    elif message.text == "Done some of the task":
        bot.send_message(message.from_user.id,
                         "Choose the index number of the task you have done when you finish send me a dot .")
        bot.register_next_step_handler(message, done_task)

    else:
        bot.send_message(message.from_user.id, "I can't understand you :(")


def get_task(message):
    global to_do_list
    global st
    text_from_user = message.text
    if message.text is not None:
        if text_from_user != '.':
            bot.send_message(message.from_user.id, 'Added')
            to_do_list.append(text_from_user)
            bot.register_next_step_handler(message, get_task)
        else:
            st = write_todo_list(to_do_list)
            bot.send_message(message.from_user.id, f"Your to-do list:\n{st}")
    else:
        bot.send_message(message.from_user.id, "I can read only text. Try again")
        bot.register_next_step_handler(message, get_task)



def done_task(message):
    global to_do_list
    global st

    text_from_user = message.text

    if message.text is not None:
        if text_from_user.isdigit() and int(text_from_user) <= len(to_do_list) and int(text_from_user) > 0:
            if int(text_from_user) <= len(to_do_list) and int(text_from_user)>0:
                to_do_list.pop(int(text_from_user)-1)
                bot.send_sticker(message.chat.id, sticker=random.choice(stickers_list))
                bot.send_message(message.from_user.id, random.choice(cheer_up_messages))

                st = write_todo_list(to_do_list)
                bot.send_message(message.from_user.id, f"Your to-do list:\n{st}")
                bot.register_next_step_handler(message, done_task)
            else:
                bot.send_message(message.from_user.id, f"You sent something incorrectly, maybe the wrong number of your task or your to-do list is empty\n Try again or send me a dot . to exit to the main menu")
                bot.register_next_step_handler(message, done_task)
        elif text_from_user == '.':
            st = write_todo_list(to_do_list)
            bot.send_message(message.from_user.id, f"Your to-do list:\n{st}")
        else:
            bot.send_message(message.from_user.id,
                             f"You sent something incorrectly, maybe the wrong number of your task or your to-do list is empty\n Try again or send me a dot . to exit to the main menu")
            bot.register_next_step_handler(message, done_task)
    else:
        bot.send_message(message.from_user.id, "I can read only text. Try again")
        bot.register_next_step_handler(message, done_task)

def write_todo_list(to_do_list):
    st = ""
    for i in range(0, len(to_do_list)):
        st += f"🗃 {i + 1}. {to_do_list[i]}\n"
    return st


bot.polling(none_stop=True, interval = 0)
