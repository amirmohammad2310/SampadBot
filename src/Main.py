import telebot
import User
import os
from telebot import types

directories = [entry for entry in os.listdir('.') if os.path.isdir(entry)]


print("hello\n\n\n\n\n\n\n")
print(directories)
TOKEN = "7287866527:AAH0jFYht54U_XMCzc_ThdcQ-KSgK9f2yHE"


bot = telebot.TeleBot(TOKEN)

current_menu = 'start'

	




@bot.message_handler(commands = ['start'])
def start_menu(message):
	if(current_menu == 'start'):
		bot.reply_to(message, "سلام خوبی؟ \n به ربات کانون خوش اومدی")
	bot.send_message(message.chat.id , "خوب حتما میخوای بدونی این ربات چیکار میکنه بزار تا بهت بگم\nto be complete")

@bot.message_handler(commands = ['help'])
def show_help(message):
	bot.reply_to(message , "عه مشکلی پیش اومده؟")
	last_sent_message = bot.send_message(message.chat.id , "خوب بزار یه لیست از دستورات بهت بدم ")
	last_sent_message = bot.reply_to(last_sent_message , "the commands lilst")
	bot.reply_to(last_sent_message ,"هنوز مشکلت حل نشده ؟ قصه نداره به پشتیبانی فنی به آیدی \"@amirmo844\" پیام بده" )

@bot.message_handler(commands = ['register'])
def register_menu(message):
	id = message.chat.id
	if(User.get_user_json(id)):
		bot.reply_to(message , "there is a account")
	else:
	    User.save_user(User.make_json_string("amir" ,"sdffas" , "sdffas", "sdffas", "sdffas", "sdffas", "sdffas"), message.chat.id)
	    bot.reply_to(message , "okey you signed up")

	

	





bot.infinity_polling()
