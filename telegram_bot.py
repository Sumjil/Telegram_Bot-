import telebot
from telebot import types
import configure

# in the future will be
# def edit_list
# when a task is done bot sends a sticker or cheer-up text

bot = telebot.TeleBot(configure.config['token'])
to_do_list =[]

@bot.message_handler(commands=['start'])
def create_list(message):

    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Create a to-do list"), types.KeyboardButton("Give me just a Sticker"))
    msg = bot.send_message(message.chat.id, "What do you want?", reply_markup= rmk)
    bot.register_next_step_handler(msg, user_answer)

def user_answer(message):

    if message.text == "Create a to-do list":
        bot.send_message(message.from_user.id,
                         "Add your tasks and when you finish send me a dot .")
        bot.register_next_step_handler(message, get_task)
    elif message.text == "Give me just a Sticker":
        bot.send_sticker(message.chat.id,
                         sticker='CAACAgIAAxkBAAEGFtJjSYwDJZN1Ht7xFNuABAo9OSZBdwAC6RsAAoV_EEnRch0GfnFH5yoE')
    else:
        bot.send_message(message.from_user.id, "I can't understand you :(")


def get_task(message):
    global to_do_list
    text_from_user = message.text
    if text_from_user != '.':
        bot.send_message(message.from_user.id, 'Added')
        to_do_list.append(text_from_user)
        bot.register_next_step_handler(message, get_task)
    else:
        st = "\n".join(to_do_list)
        bot.send_message(message.from_user.id, f"Your to-do list:\n{st}")

bot.polling(none_stop=True, interval = 0)