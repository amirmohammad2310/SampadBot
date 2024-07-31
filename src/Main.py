import telebot
import User
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import food_reminder
from datetime import datetime
import schedule
import threading



TOKEN = "7287866527:AAH0jFYht54U_XMCzc_ThdcQ-KSgK9f2yHE"


bot = telebot.TeleBot(TOKEN)





def check_for_message():
    dict_weekly = food_reminder.read_weekly_dic()
    result_list = list()
    dt = datetime.now()
    day_number = dt.weekday()
    for key in dict_weekly.keys():
        if day_number == dict_weekly[key]:
            result_list.append(key)
    return result_list

      
def send_food_message():
    id_list = check_for_message()
    for id in id_list:
        bot.send_message(id , "غذا یادت نره")


def thread_for_run():
    
    schedule.every(1).day.at("19:00").do(send_food_message)

    while True:
        schedule.run_pending()



t= threading.Thread(target=thread_for_run)
t.start()



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
	elif(message.text == '/logout'):
		log_out_menu(message)
	elif(message.text == '/login'):
		login_menu(message)
	elif(message.text == '/remind'):
		remind_menu(message)
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
	elif(current_menu == 'login_phone_number'):
		login_phone_number_input(message)
	elif(current_menu == 'login_password'):
		login_password_input(message)

	
global keyboard 
global button1
global button2
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
	if(User.is_user_logged_in_with_id(id)):
		information = User.get_user_json_from_file_id(id)
		bot.reply_to(message , f"شما قبلا با شماره تماس {information['phone_number']}" )
	
	else:
		client = User.get_client_by_id(message.chat.id)
		client.current_menu = "firstname"
		bot.reply_to(message , "نام خود را وارد کنید")
	    		
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
	elif(User.is_user_exist_with_phone_number(message.text) == True):
		bot.send_message(message.chat.id , "این شماره قبلا ثبت نام کرده است")
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
		

		keyboard = InlineKeyboardMarkup()
		button1 = InlineKeyboardButton("خیر هنوز عضو نشدم", callback_data="NO")
		button2 = InlineKeyboardButton("آره بابا عضو قدیمی ام", callback_data="YES")
		keyboard.add(button1, button2)
		bot.send_message(message.chat.id, 'آیا عضو گروه سمپاد هستید؟', reply_markup=keyboard)

def group_call_handler(call):
	if(call.data == "YES" or call.data == "NO"):
		return True
	else :
		return False


@bot.callback_query_handler(group_call_handler)
def is_in_group(call):
	client = User.get_client_by_id(call.message.chat.id)
	if call.data == "YES":
		client.is_in_group = True ;
		bot.send_message(call.message.chat.id, "عضو هستم انتخاب شد")
		
	elif call.data == "NO":
		client.is_in_group = False ;
		bot.send_message(call.message.chat.id, "عضو نیستم انتخاب شد و درخواست شما برای ادمین فرستاده شد ")
	User.save_client_to_database(client)
	bot.send_message(client.id , "ثبت نام شما کامل شد و اطلاعات شما ثبت شد")
	bot.send_message('-1002215173178'  ,client.firstname +'\n'+ client.lastname +'\n'+ client.phone_number +'\n'+ client.graduation_year +'\n'+ client.field_of_study  +'\n'+ client.password +'\n'+ str(client.is_in_group))
	client.current_menu="main_menu"
	bot.edit_message_reply_markup(chat_id= call.message.chat.id , message_id=call.message.message_id, reply_markup=None)
	
def log_out_menu(message):
	if(User.is_user_logged_in_with_id(message.chat.id)):
		User.get_client_by_id(message.chat.id).current_menu = "start"
		User.rename_file_for_logout(message.chat.id)
		bot.send_message(message.chat.id , "شما از حساب خود خارج شدید")
	else:
		bot.send_message(message.chat.id , "شما داخل هیچ حسابی نیستید")
	
def login_menu(message):
	if(User.is_user_logged_in_with_id(message.chat.id)):
		bot.send_message(message.chat.id , "شما هم اکنون در یک حساب کاربری هستید")
	else:
		client = User.get_client_by_id(message.chat.id)
		client.current_menu = "login_phone_number"
		bot.reply_to(message ,  "لطفا شماره تماس خود را وارد کنید")

def login_phone_number_input(message):
	if((User.is_phone_number_valid(message.text)) == False):
		bot.send_message(message.chat.id , "لطفا یک شماره تلفن همراه معتبر به همراه صفر در اولش بنویسید")
	elif(User.is_user_exist_with_phone_number(message.text) == False):
		bot.send_message(message.chat.id , "تا حالا این شماره ثبت نشده است")
	else:
		client = User.get_client_by_id(message.chat.id)
		client.phone_number = message.text
		bot.send_message(client.id , "رمز عبور خود را بنویسید")
		client.current_menu = 'login_password'
		
def login_password_input(message):
	s = User.get_user_json_from_file_phone_number(User.get_client_by_id(message.chat.id).phone_number)
	if(s['password'] != message.text):
		bot.send_message(message.chat.id , "رمز عبور اشتباه است")
	else:
		User.rename_file_for_login(User.get_client_by_id(message.chat.id).phone_number , message.chat.id)
		bot.send_message(message.chat.id , "با موفقیت وارد شدید")


def remind_menu(message):
	if(User.is_user_logged_in_with_id(message.chat.id)):
		if str(message.chat.id in food_reminder.read_weekly_dic()):
			keyboard = InlineKeyboardMarkup()
			button1 = InlineKeyboardButton("شنبه", callback_data="5")
			button2 = InlineKeyboardButton("یک شنبه", callback_data="6")
			button3 = InlineKeyboardButton("دوشنبه", callback_data="0")
			button4 = InlineKeyboardButton("سه شنبه", callback_data="1")
			button5 = InlineKeyboardButton("چهار شنبه", callback_data="2")
			keyboard.add(button1, button2, button3, button4, button5)
			bot.send_message(message.chat.id, 'دوست داری چه روزی بهت یاد آوری بشه؟', reply_markup=keyboard)
	else:
		bot.send_message(message.chat.id , "شما داخل هیچ حسابی نیستید")

def remind_food_handler(call):
	if call.data == "5":
		return True
	elif call.data == "6":
		return True
	elif call.data == "0":
		return True
	elif call.data == "1":
		return True
	elif call.data == "2":
		return True
	else:
		return False


def add_weekly(id, number_of_day):
    with open("../data/weeklyschedule.json", "r") as file:
        dict_weekly = json.load(file)

    dict_weekly[id] = number_of_day
    str_weekly = json.dumps(dict_weekly)
   
    with open("../data/weeklyschedule.json", "w") as file1:
        file1.write(str_weekly)

		
@bot.callback_query_handler(remind_food_handler)
def remind_food(call):
	if call.data == "5":
		add_weekly(call.message.chat.id , 5)
	elif call.data == "6":
		add_weekly(call.message.chat.id , 6)
	elif call.data == "0":
		add_weekly(call.message.chat.id , 0)
	elif call.data == "1":
		add_weekly(call.message.chat.id , 1)
	elif call.data == "2":
		add_weekly(call.message.chat.id , 2)
	bot.send_message(call.message.chat.id , "انتخاب شما ثبت شد")
	bot.edit_message_reply_markup(chat_id= call.message.chat.id , message_id=call.message.message_id, reply_markup=None)

bot.infinity_polling()
