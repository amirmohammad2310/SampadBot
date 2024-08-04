import telebot
import User
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import food_reminder
from datetime import datetime
import schedule
import threading
import requests as req
import re
import os

TOKEN = "7287866527:AAH0jFYht54U_XMCzc_ThdcQ-KSgK9f2yHE"

bot = telebot.TeleBot(TOKEN)


# def check_for_message():
#     dict_weekly = food_reminder.read_weekly_dic()
#     result_list = list()
#     dt = datetime.now()
#     day_number = dt.weekday()
#     for key in dict_weekly.keys():
#         if day_number == dict_weekly[key]:
#             result_list.append(key)
#     return result_list


# def send_food_message():
#     id_list = check_for_message()
#     for id in id_list:
#         bot.send_message(id , "غذا یادت نره")


# def thread_for_run():

#     schedule.every(1).day.at("19:00").do(send_food_message)

#     while True:
#         schedule.run_pending()


# t= threading.Thread(target=thread_for_run)
# t.start()


def is_user_logged_in_with_id(id_input):
    id_str = str('_' + str(id_input))  # Renamed 'id' to 'id_str' to avoid shadowing

    for filename in os.listdir('../data/'):
        if re.search(id_str, filename):
            with open("../data/" + filename, "r") as file:
                data_dict = json.load(file)

            client = User.get_client_by_id(id_input)
            client.firstname = data_dict["firstname"]
            client.lastname = data_dict["lastname"]
            client.phone_number = data_dict["phone_number"]
            client.graduation_year = data_dict["graduation_year"]
            client.field_of_study = data_dict["field_of_study"]
            client.password = data_dict["password"]
            return True

    return False


@bot.message_handler(func=lambda message: True)
def message_handle(message):
    if (User.get_client_by_id(message.chat.id) == False):
        User.client(message.chat.id)
        current_menu = 'start'
    else:
        client = User.get_client_by_id(message.chat.id)
        current_menu = client.current_menu
    if (message.text == '/start'):
        start_menu(message)
    elif (message.text == '/help'):
        show_help(message)
    elif (message.text == '/register'):
        register_menu(message)
    elif (message.text == '/logout'):
        log_out_menu(message)
    elif (message.text == '/login'):
        login_menu(message)
    elif (message.text == '/remind'):
        remind_menu(message)
    elif (message.text == '/chat'):
        chat_ai_menu(message)
    elif (message.text == '/anonymous'):
        chat_anonymous(message)
    elif (message.text == '/show_profile'):
        show_profile(message)
    elif (message.text == '/edit_profile'):
        edit_profile(message)
    elif (current_menu == 'firstname'):
        firstname_input(message)
    elif (current_menu == 'lastname'):
        lastname_input(message)
    elif (current_menu == 'phone_number'):
        phone_number_input(message)
    elif (current_menu == 'graduation'):
        graduation_year_input(message)
    elif (current_menu == 'field'):
        field_of_study_input(message)
    elif (current_menu == 'password'):
        password_input(message)
    elif (current_menu == 'repassword'):
        re_password_input(message)
    elif (current_menu == 'login_phone_number'):
        login_phone_number_input(message)
    elif (current_menu == 'login_password'):
        login_password_input(message)
    elif (current_menu == 'chat_ai'):
        chat_respon(message)
    elif (current_menu == 'chat_anonymous'):
        print("here1")
        chat_anonymous_respon(message)


    match current_menu:
        case "edit_firstname":
            edit_firstname(message)
        case "edit_lastname":
            edit_lastname(message)
        case "edit_phonenumber":
            edit_phone_number(message)
        case "edit_graduation_year":
            edit_graduation_year(message)
        case "edit_field_of_study":
            edit_field_of_study(message)
        case "edit_password":
            edit_password(message)
        case "edit_repassword":
            edit_repassword_password(message)


global keyboard
global button1
global button2


def start_menu(message):
    bot.reply_to(message, "سلام خوبی؟ \n به ربات کانون خوش اومدی")
    bot.send_message(message.chat.id, "خوب حتما میخوای بدونی این ربات چیکار میکنه بزار تا بهت بگم\nto be complete")


def show_help(message):
    bot.reply_to(message, "عه مشکلی پیش اومده؟")
    last_sent_message = bot.send_message(message.chat.id, "خوب بزار یه لیست از دستورات بهت بدم ")
    last_sent_message = bot.reply_to(last_sent_message, "the commands lilst")
    bot.reply_to(last_sent_message, "هنوز مشکلت حل نشده ؟ قصه نداره به پشتیبانی فنی به آیدی \"@amirmo844\" پیام بده")


def register_menu(message):
    id = message.chat.id
    if (is_user_logged_in_with_id(id)):

        information = User.get_user_json_from_file_id(id)
        bot.reply_to(message, f"شما قبلا با شماره تماس {information['phone_number']}")

    else:
        client = User.get_client_by_id(message.chat.id)
        client.current_menu = "firstname"
        bot.reply_to(message, "نام خود را وارد کنید")


def firstname_input(message):
    client = User.get_client_by_id(message.chat.id)
    client.firstname = message.text
    bot.reply_to(message, f'نام کوچک شما {message.text} ثبت شد')
    bot.send_message(client.id, "لطفا فامیلی تو بنویس")
    client.current_menu = 'lastname'


def lastname_input(message):
    client = User.get_client_by_id(message.chat.id)
    client.lastname = message.text
    bot.reply_to(message, f'نام فامیلی شما {message.text} ثبت شد')
    bot.send_message(client.id, "لطفا شماره تلفنتو بنویس")
    client.current_menu = 'phone_number'


def phone_number_input(message):
    if ((User.is_phone_number_valid(message.text)) == False):
        bot.send_message(message.chat.id, "لطفا یک شماره تلفن همراه معتبر به همراه صفر در اولش بنویسید")
    elif (User.is_user_exist_with_phone_number(message.text) == True):
        bot.send_message(message.chat.id, "این شماره قبلا ثبت نام کرده است")
    else:
        client = User.get_client_by_id(message.chat.id)
        client.phone_number = message.text
        bot.reply_to(message, f'شماره تماس شما {message.text} ثبت شد')
        bot.send_message(client.id, "لطفا سال فارغ التحصیلیت رو بنویس")
        client.current_menu = 'graduation'


def graduation_year_input(message):
    if ((User.is_graduation_valid(message.text)) == False):
        bot.send_message(message.chat.id, "لطفا یک عدد چهار رقمی درست وارد کن")
    else:
        client = User.get_client_by_id(message.chat.id)
        client.graduation_year = message.text
        bot.reply_to(message, f'زمان فارغ التحصیلی  شما {message.text} ثبت شد')
        bot.send_message(client.id, "لطفا رشته التحصیلیت رو بنویس")
        client.current_menu = 'field'


def field_of_study_input(message):
    client = User.get_client_by_id(message.chat.id)
    client.field_of_study = message.text
    bot.reply_to(message, f'رشته تحصیلی شما {message.text} ثبت شد')
    bot.send_message(client.id, "لطفا رمز عبورتو بنویس بنویس")
    client.current_menu = 'password'


def password_input(message):
    client = User.get_client_by_id(message.chat.id)
    client.password = message.text
    bot.send_message(client.id, "لطفا تکرار رمز عبورتو بنویس بنویس")
    client.current_menu = 'repassword'


def re_password_input(message):
    client = User.get_client_by_id(message.chat.id)
    if (client.password != message.text):
        bot.send_message(message.chat.id, "رمز عبور با رمز عبور اولیه مطابقت نداره")
    else:
        bot.reply_to(message, f'رمز عبور   شما {message.text} ثبت شد')

        keyboard = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("خیر هنوز عضو نشدم", callback_data="NO")
        button2 = InlineKeyboardButton("آره بابا عضو قدیمی ام", callback_data="YES")
        keyboard.add(button1, button2)
        bot.send_message(message.chat.id, 'آیا عضو گروه سمپاد هستید؟', reply_markup=keyboard)


def group_call_handler(call):
    if (call.data == "YES" or call.data == "NO"):
        return True
    else:
        return False


@bot.callback_query_handler(group_call_handler)
def is_in_group(call):
    client = User.get_client_by_id(call.message.chat.id)
    if call.data == "YES":
        client.is_in_group = True;
        bot.send_message(call.message.chat.id, "عضو هستم انتخاب شد")

    elif call.data == "NO":
        client.is_in_group = False;
        bot.send_message(call.message.chat.id, "عضو نیستم انتخاب شد و درخواست شما برای ادمین فرستاده شد ")
    User.save_client_to_database(client)
    bot.send_message(client.id, "ثبت نام شما کامل شد و اطلاعات شما ثبت شد")
    bot.send_message('-1002215173178',
                     '#ورودی' + "\n" + client.firstname + '\n' + client.lastname + '\n' + client.phone_number + '\n' + client.graduation_year + '\n' + client.field_of_study + '\n' + client.password + '\n' + str(
                         client.is_in_group))
    client.current_menu = "main_menu"
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def log_out_menu(message):
    if (is_user_logged_in_with_id(message.chat.id)):
        User.get_client_by_id(message.chat.id).current_menu = "start"
        User.rename_file_for_logout(message.chat.id)
        bot.send_message(message.chat.id, "شما از حساب خود خارج شدید")
    else:
        bot.send_message(message.chat.id, "شما داخل هیچ حسابی نیستید")


def login_menu(message):
    if (is_user_logged_in_with_id(message.chat.id)):
        bot.send_message(message.chat.id, "شما هم اکنون در یک حساب کاربری هستید")
    else:
        client = User.get_client_by_id(message.chat.id)
        client.current_menu = "login_phone_number"
        bot.reply_to(message, "لطفا شماره تماس خود را وارد کنید")


def login_phone_number_input(message):
    if ((User.is_phone_number_valid(message.text)) == False):
        bot.send_message(message.chat.id, "لطفا یک شماره تلفن همراه معتبر به همراه صفر در اولش بنویسید")
    elif (User.is_user_exist_with_phone_number(message.text) == False):
        bot.send_message(message.chat.id, "تا حالا این شماره ثبت نشده است")
    else:
        client = User.get_client_by_id(message.chat.id)
        client.phone_number = message.text
        bot.send_message(client.id, "رمز عبور خود را بنویسید")
        client.current_menu = 'login_password'


def login_password_input(message):
    s = User.get_user_json_from_file_phone_number(User.get_client_by_id(message.chat.id).phone_number)
    if (s['password'] != message.text):
        bot.send_message(message.chat.id, "رمز عبور اشتباه است")
    else:
        client = User.get_client_by_id(message.chat.id)
        User.rename_file_for_login(client.phone_number, message.chat.id)
        if(os.path.exists("../data/" + str(client.phone_number) + '_' + str(client.id)+".json")):
            with open("../data/" + str(client.phone_number) + '_' + str(client.id)+".json", "r") as file:
                dict = json.load(file)

            client.firstname = dict["firstname"]
            client.lastname = dict["lastname"]
            client.graduation_year = dict["graduation_year"]
            client.field_of_study = dict["field_of_study"]
            client.password = dict["password"]

            bot.send_message(message.chat.id, "با موفقیت وارد شدید")
        else:
            bot.send_message(message.chat.id , "شما با یک حساب دیگر در وارد شده اید")


def remind_menu(message):
    if (is_user_logged_in_with_id(message.chat.id)):
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
        bot.send_message(message.chat.id, "شما داخل هیچ حسابی نیستید")


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
        add_weekly(call.message.chat.id, 5)
    elif call.data == "6":
        add_weekly(call.message.chat.id, 6)
    elif call.data == "0":
        add_weekly(call.message.chat.id, 0)
    elif call.data == "1":
        add_weekly(call.message.chat.id, 1)
    elif call.data == "2":
        add_weekly(call.message.chat.id, 2)
    bot.send_message(call.message.chat.id, "انتخاب شما ثبت شد")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


def chat_ai_menu(message):
    if (is_user_logged_in_with_id(message.chat.id)):
        bot.send_message(message.chat.id,
                         "سلام شما وارد بخش هوش مصنوعی بات شدید و می تونید با هوش مصنوعی چت کنید برای خروج بنویسید\"تمام\" ")
        User.get_client_by_id(message.chat.id).current_menu = 'chat_ai'
    else:
        bot.send_message(message.chat.id,
                         "اول باید یه اکانت بسازی و رایگان از چت با هوش مصنوعی استفاده کنی از دستور /register برای ثبت نام و از دستور /login برای ورود استفاده کن")


def chat_respon(message):
    q = message.text
    if q == 'تمام':
        bot.reply_to(message, 'موفق باشی عزیز')
        User.get_client_by_id(message.chat.id).current_menu = 'start'
    else:
        bot.reply_to(message.chat.id, "این بخش به دلیل مشکلات هاستینگ هنوز غیر فعال است با نوشتن  \"تمام\"خارج شوید")
        return
        out = req.get('http://5.161.91.18/chat?text=' + q)
        bot.reply_to(message, out)


def chat_anonymous(message):
    if (is_user_logged_in_with_id(message.chat.id)):
        bot.send_message(message.chat.id,
                         "سلام شما وارد بخش چت ناشناس بات شده اید میتوانید انتقاداتتونو ناشناس برای ما بفرستید تضمین میشود هیچ راه شناسایی از شما برای ادمین ها وجود ندارد برای خروج بنویسید\"تمام\" ")
        User.get_client_by_id(message.chat.id).current_menu = 'chat_anonymous'
    else:
        bot.send_message(message.chat.id,
                         "اول باید یه اکانت بسازی بعد میتونی پیام بدی /register برای ثبت نام و از دستور /login برای ورود استفاده کن")



def chat_anonymous_respon(message):
    q = message.text
    if q == 'تمام':
        bot.reply_to(message, 'موفق باشی عزیز انتقاد شما به گوش ادمین ها میرسه حتما')
        User.get_client_by_id(message.chat.id).current_menu = 'start'
    else:
        print("here2")
        bot.send_message('-1002215173178', "#انتقاد" + "\n" + message.text + '\n' + str(message.chat.id))


def show_profile(message):
    if (is_user_logged_in_with_id(message.chat.id)):
        client = User.get_client_by_id(message.chat.id)
        bot.send_message(message.chat.id,
                         "\n" + client.firstname + '\n' + client.lastname + '\n' + client.phone_number + '\n' + client.graduation_year + '\n' + client.field_of_study)
    else:
        bot.send_message(message.chat.id,
                         "اول باید یه اکانت بسازی /register برای ثبت نام و از دستور /login برای ورود استفاده کن")


def edit_profile(message):
    if(is_user_logged_in_with_id(message.chat.id)):
        keyboard = InlineKeyboardMarkup()
        button_edit_1 = InlineKeyboardButton("نام کوچک", callback_data="edit_firstname")
        button_edit_2 = InlineKeyboardButton("فامیلی", callback_data="edit_lastname")
        button_edit_3 = InlineKeyboardButton("شماره تلفن", callback_data="edit_phonenumber")
        button_edit_4 = InlineKeyboardButton("سال فارغ التحصیلی", callback_data="edit_graduation_year")
        button_edit_5 = InlineKeyboardButton("رشته تحصیلی", callback_data="edit_field_of_study")
        button_edit_6 = InlineKeyboardButton("رمز عبور", callback_data="edit_password")
        button_edit_7 = InlineKeyboardButton("ثبت اطلاعات", callback_data="edit_confrim")
        keyboard.add(button_edit_1, button_edit_2, button_edit_3, button_edit_4, button_edit_5, button_edit_6,button_edit_7)
        bot.send_message(message.chat.id,
                     'کدام اطلاعات نیاز به ادیت داره؟ حتما بعد از ثتب اطلاعات کلید ثبت رو بزن تا اطلاعاتت ثبت بشن',
                     reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "اول باید یه اکانت بسازی /register برای ثبت نام و از دستور /login برای ورود استفاده کن")


@bot.callback_query_handler(lambda call: re.search("edit_.+", call.data))
def edit_menu(call):
    client = User.get_client_by_id(call.message.chat.id)
    client.current_menu = call.data
    match call.data:
        case "edit_firstname":
            bot.send_message(call.message.chat.id, "نام کوچک خودرا وارد کنید")
        case "edit_lastname":
            bot.send_message(call.message.chat.id, "نام فامیلی خودرا وارد کنید")
        case "edit_phonenumber":
            bot.send_message(call.message.chat.id, "شماره تماس خودرا وارد کنید")
        case "edit_graduation_year":
            bot.send_message(call.message.chat.id, "سال فارغ التحصیلی خودرا وارد کنید")
        case "edit_field_of_study":
            bot.send_message(call.message.chat.id, "رشته خودرا وارد کنید")
        case "edit_password":
            bot.send_message(call.message.chat.id, "رمز عبور خودرا وارد کنید")
        case "edit_confrim":
            client = User.get_client_by_id(call.message.chat.id)
            User.delet_user_with_id(call.message.chat.id)
            User.save_client_to_database(client)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=None)
            bot.send_message(call.message.chat.id, 'تغییرات شما نهایی شد')


def edit_firstname(message):
    client = User.get_client_by_id(message.chat.id)
    client.firstname = message.text
    bot.reply_to(message, f'نام کوچک شما {message.text} ثبت شد')
    client.current_menu = 'main_menu'


def edit_lastname(message):
    client = User.get_client_by_id(message.chat.id)
    client.lastname = message.text
    bot.reply_to(message, f'نام فامیلی شما {message.text} ثبت شد')
    client.current_menu = 'main_menu'


def edit_phone_number(message):
    client = User.get_client_by_id(message.chat.id)
    if not (User.is_phone_number_valid(message.text)):
        bot.send_message(message.chat.id, "لطفا یک شماره تلفن همراه معتبر به همراه صفر در اولش بنویسید")
    elif User.is_user_exist_with_phone_number(message.text) == True and client.phone_number != message.text:
        bot.send_message(message.chat.id, "این شماره قبلا ثبت نام کرده است")
    else:
        client.phone_number = message.text
        bot.reply_to(message, f'شماره تماس شما {message.text} ثبت شد')
        client.current_menu = 'main_menu'


def edit_graduation_year(message):
    if ((User.is_graduation_valid(message.text)) == False):
        bot.send_message(message.chat.id, "لطفا یک عدد چهار رقمی درست وارد کن")
    else:
        client = User.get_client_by_id(message.chat.id)
        client.graduation_year = message.text
        bot.reply_to(message, f'زمان فارغ التحصیلی  شما {message.text} ثبت شد')
    client.current_menu = 'main_menu'


def edit_field_of_study(message):
    client = User.get_client_by_id(message.chat.id)
    client.field_of_study = message.text
    bot.reply_to(message, f'رشته تحصیلی شما {message.text} ثبت شد')
    client.current_menu = 'main_menu'


def edit_password(message):
    s = User.get_user_json_from_file_id(message.chat.id)
    if (s['password'] != message.text):
        bot.send_message(message.chat.id, "رمز عبور اشتباه است")
    else:
        client = User.get_client_by_id(message.chat.id)
        bot.send_message(message.chat.id, "حالا رمز عبور جدید رو بنویس")
        client.current_menu = 'edit_repassword'


def edit_repassword_password(message):
    client = User.get_client_by_id(message.chat.id)
    client.password = message.text
    bot.send_message(client.id, "رمز عبور جدید ثتب شد برای ثبت نهایی کلید ثبت نهایی رو بزن")
    client.current_menu = 'main_menu'


bot.infinity_polling()
