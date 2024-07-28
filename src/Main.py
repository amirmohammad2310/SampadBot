import telebot
import User
from telebot import types


TOKEN = "7287866527:AAH0jFYht54U_XMCzc_ThdcQ-KSgK9f2yHE"


bot = telebot.TeleBot(TOKEN)




@bot.message_handler(func=lambda message: True)
def message_handle(message):
	if(User.get_client_by_id(message.chat.id) == False):
		current_menu = 'start'
	else:
		client = User.get_client_by_id(message.chat.id)
		current_menu =client.current_menu
	if(message.text == '/start'):
		start_menu(message)
	elif(message.text == '/help'):
		show_help(message)
	elif(message.text == '/register'):
		register_menu(message)
	elif(current_menu == 'firstname'):
		firstname_input(message)

	








def start_menu(message):
	bot.reply_to(message, "سلام خوبی؟ \n به ربات کانون خوش اومدی")
	bot.send_message(message.chat.id , "خوب حتما میخوای بدونی این ربات چیکار میکنه بزار تا بهت بگم\nto be complete")
	User.client(message.chat.id)
	




def show_help(message):
	bot.reply_to(message , "عه مشکلی پیش اومده؟")
	last_sent_message = bot.send_message(message.chat.id , "خوب بزار یه لیست از دستورات بهت بدم ")
	last_sent_message = bot.reply_to(last_sent_message , "the commands lilst")
	bot.reply_to(last_sent_message ,"هنوز مشکلت حل نشده ؟ قصه نداره به پشتیبانی فنی به آیدی \"@amirmo844\" پیام بده" )

def register_menu(message):
	id = message.chat.id
	if(User.is_user_json(id)):
		information = User.get_user_json(id)
		bot.reply_to(message , information.get("firstname") )
	
	else:
		client = User.get_client_by_id(message.chat.id)
		client.current_menu = "firstname"
		bot.reply_to(message , "enter your first name")
	    
		
		
def firstname_input(message):
	bot.reply_to(message , message.text)
	

	





bot.infinity_polling()
