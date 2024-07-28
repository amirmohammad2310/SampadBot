import telebot
import User
import re


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
	elif(current_menu == 'lastname'):
		lastname_input(message)
	elif(current_menu == 'phone_number'):
		phone_number_input(message)
	elif(current_menu == 'graduation'):
		graduation_year_input(message)
	elif(current_menu == 'field'):
		field_of_study_input(message)
	elif(current_menu == 'password'):
		password_input(message)
	elif(current_menu == 'repassword'):
		re_password_input(message)
	

	



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
	if(User.is_user_exist_with_id(id)):
		information = User.get_user_json_from_file(id)
		bot.reply_to(message , f"شما قبلا با شماره تماس {information.['phone_number']}" )
	
	else:
		client = User.get_client_by_id(message.chat.id)
		client.current_menu = "firstname"
		bot.reply_to(message , "enter your first name")
	    		
def firstname_input(message):
	client = User.get_client_by_id(message.chat.id)
	client.firstname = message.text
	bot.reply_to(message , f'نام کوچک شما {message.text} ثبت شد')
	bot.send_message(client.id , "لطفا فامیلی تو بنویس")
	client.current_menu = 'lastname'
	
def lastname_input(message):
	client = User.get_client_by_id(message.chat.id)
	client.lastname = message.text
	bot.reply_to(message , f'نام فامیلی شما {message.text} ثبت شد')
	bot.send_message(client.id , "لطفا شماره تلفنتو بنویس")
	client.current_menu = 'phone_number'

def phone_number_input(message):
	if((User.is_phone_number_valid(message.text)) == False):
		bot.send_message(message.chat.id , "لطفا یک شماره تلفن همراه معتبر به همراه صفر در اولش بنویسید")
	else:
		client = User.get_client_by_id(message.chat.id)
		client.phone_number = message.text
		bot.reply_to(message , f'شماره تماس شما {message.text} ثبت شد')
		bot.send_message(client.id , "لطفا سال فارغ التحصیلیت رو بنویس")
		client.current_menu = 'graduation'

def graduation_year_input(message):
	if((User.is_graduation_valid(message.text)) == False):
		bot.send_message(message.chat.id , "لطفا یک عدد چهار رقمی درست وارد کن")
	else:
		client = User.get_client_by_id(message.chat.id)
		client.graduation_year = message.text
		bot.reply_to(message , f'زمان فارغ التحصیلی  شما {message.text} ثبت شد')
		bot.send_message(client.id , "لطفا رشته التحصیلیت رو بنویس")
		client.current_menu = 'field'

def field_of_study_input(message):
	client = User.get_client_by_id(message.chat.id)
	client.field_of_study = message.text
	bot.reply_to(message , f'رشته تحصیلی شما {message.text} ثبت شد')
	bot.send_message(client.id , "لطفا رمز عبورتو بنویس بنویس")
	client.current_menu = 'password'

def password_input(message):
	client = User.get_client_by_id(message.chat.id)
	client.password = message.text
	bot.send_message(client.id , "لطفا تکرار رمز عبورتو بنویس بنویس")
	client.current_menu = 'repassword'

def re_password_input(message):
	client = User.get_client_by_id(message.chat.id)
	if(client.password != message.text):
		bot.send_message(message.chat.id , "رمز عبور با رمز عبور اولیه مطابقت نداره")
	else:
		bot.reply_to(message , f'رمز عبور   شما {message.text} ثبت شد')
		User.save_client_to_database(client)
		bot.send_message(client.id , "ثبت نام شما کامل شد و اطلاعات شما ثبت شد")
		client.current_menu="main_menu"

def log_out_menu(message):
	
	





bot.infinity_polling()
