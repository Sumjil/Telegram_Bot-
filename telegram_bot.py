import telebot
from telebot import types
import configure

bot = telebot.TeleBot(configure.config['token'])


@bot.message_handler(commands=['start']) 
def create_list(message):

    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Create a note"), types.KeyboardButton("Sticker"))
    msg = bot.send_message(message.chat.id, "What do you want?", reply_markup= rmk)
    bot.register_next_step_handler(msg, user_answer)




def user_answer(message):

    if message.text == "Create a note":
        msg = bot.send_message(message.chat.id, "Write want you want....")
        bot.register_next_step_handler(msg,user_to_do_list)
    elif message.text == "Sticker":
        bot.send_sticker(message.chat.id,
                         sticker='CAACAgIAAxkBAAEGFtJjSYwDJZN1Ht7xFNuABAo9OSZBdwAC6RsAAoV_EEnRch0GfnFH5yoE')
    else:
        bot.send_message(message.chat.id, "I can't understand you")

def user_to_do_list(message):
    bot.send_message(message.chat.id,f"Your note: {message.text}")


bot.polling(none_stop=True, interval = 0)