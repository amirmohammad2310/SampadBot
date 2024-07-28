import telebot

from telebot import types

TOKEN = "7287866527:AAH0jFYht54U_XMCzc_ThdcQ-KSgK9f2yHE"


bot = telebot.TeleBot(TOKEN)

current_menu = 'start'

	




@bot.message_handler(commands = ['start'])
def start_menu(message):
	if(current_menu == 'start')
		bot.reply_to(message, "سلام خوبی؟ \n به ربات کانون خوش اومدی")
	bot.send_message(message.chat.id , "خوب حتما میخوای بدونی این ربات چیکار میکنه بزار تا بهت بگم\nto be complete")







bot.infinity_polling()
