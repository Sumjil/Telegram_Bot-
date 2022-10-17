import telebot
from telebot import types
import configure
import random

bot = telebot.TeleBot(configure.config['token'])
to_do_list =[]
sticker_list = ["CAACAgIAAxkBAAEGFtBjSYtM9FIi9cEPFqefgDfff-saNwACfRQAAgIKKUjcktjW3H-y1yoE","CAACAgIAAxkBAAEGFtJjSYwDJZN1Ht7xFNuABAo9OSZBdwAC6RsAAoV_EEnRch0GfnFH5yoE","CAACAgIAAxkBAAEGH-xjTcb4P8GORiphnySen2Lt1A8_pwACAR4AArk8OUjrraQbd6DLgioE","CAACAgIAAxkBAAEGH-1jTcb4qxPDVBSOwxMQDK8HqMArEAACdB0AAoBAEEk4PdJUj_G_ISoE","CAACAgIAAxkBAAEGH_NjTcb4Ia2t0fSxUEho_0J_faGvbwACZyEAAvkIkElcqMp3Bqm4mCoE"]
st = ""

@bot.message_handler(commands=['start'])
def create_list(message):

    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Create a to-do list"))
    rmk.add(types.KeyboardButton("Show me my to-do list"))
    rmk.add(types.KeyboardButton("Done some of the task"))
    msg = bot.send_message(message.chat.id, "What do you want?", reply_markup= rmk)
    bot.register_next_step_handler(msg, user_answer)

@bot.message_handler(content_types=['text'])
def user_answer(message):

    if message.text == "Create a to-do list":
        bot.send_message(message.from_user.id,
                         "Add your tasks and when you finish send me a dot .")
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
    if text_from_user != '.':
        bot.send_message(message.from_user.id, 'Added')
        to_do_list.append("🗃"+text_from_user)
        bot.register_next_step_handler(message, get_task)
    else:
        st = "\n".join(to_do_list)
        bot.send_message(message.from_user.id, f"Your to-do list:\n{st}")

def done_task(message):
    text_from_user = message.text
    if text_from_user != '.':
        bot.send_sticker(message.chat.id, sticker=random.choice(sticker_list))
        bot.send_message(message.from_user.id, "Wooooow, you are amazing! Keep going!")
        to_do_list.pop(int(text_from_user)-1)
        bot.register_next_step_handler(message, done_task)
    else:
        st = "\n".join(to_do_list)
        bot.send_message(message.from_user.id, f"Your to-do list:\n{st}")


bot.polling(none_stop=True, interval = 0)