import telebot
from telebot import types
import os

token = '5888317959:AAEDUQmo-_FhORf6MS2hEC0jh4-BKQ5ncfA'

bot = telebot.TeleBot(token)

path = "/home/telegram_bot/data"
#path = "/home/sergey/Stuff/telegram_bot/data"
vec = list()
depth = 0

#variaty = ["задания", "расписание"]
variaty = ["задания"]
subjects = ["назад", "физика"]
phisic_olimpiads = ["назад", "физтех", "росатом"]
grades = ["назад", "11", "10"]
years = ["назад", "2021", "2020", "2019", "2018"]


def OpenForStart(n):
    global path
    file_path = path + '/' + "Users" + '/' + str(n) + '.txt'
    file = open(file_path, 'w')
    file.write('0\n')
    file.close()
    
def OpenToRead(n):
    global path
    global depth
    global vec
    file_path = path + '/' + "Users" + '/' + str(n) + '.txt'
    f = open(file_path)
    lines = f.readlines()
    f.close()
    depth = int(lines[0][0])
    vec = list()
    for word in lines[1:]:
        vec.append(word[:-1])
    
def OpenToWrite(n):
    global path
    global depth
    global vec
    file_path = path + '/' + "Users" + '/' + str(n) + '.txt'
    file = open(file_path, 'w')
    file.write(str(depth) + '\n')
    for word in vec:
        file.write(word + '\n')
    file.close()

def make_buttons(message, text, lst):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    global depth
    for name in lst:
        markup.add(types.KeyboardButton(name))
    bot.send_message(message.chat.id, text, reply_markup = markup)

def make_path():
    global path
    global vec
    pth = path
    for i in vec:
        pth += "/" + i
    return pth

@bot.message_handler(commands=['start'])
def start(message, res=False):
    OpenForStart(message.chat.id)  # make all data equals to preset values
    make_buttons(message, "Привет! Этот бот поможет тебе найти задания прошлых лет из различных олимпиад: нажимай 'задания', и поехали!", variaty)

def Back(message):
    global depth
    global vec
    
    depth -=1
    vec.pop()
    if depth == 0:
        start(message, res=False)
    else:
        message.text = vec[-1]
        vec.pop()
        if depth == 1:
            Zero(message)
        elif depth == 2:
            One(message)
        elif depth == 3:
            Two(message)

def Zero(message):
    global vec
    global depth
    m = message.text.lower()
    if m in variaty:
        vec.append(m)
        depth = 1
        if m == "задания":
            make_buttons(message, "Выбери предмет", subjects)
        elif m == "расписание":
            make_buttons(message, "Do something with schedual", ["DoSomething"])
    else:
        bot.send_message(message.chat.id, "Я сломался на 0 шаге \nНапиши '/start', чтобы починить меня!")

def One(message):
    global vec
    global depth
    m = message.text.lower()
    if m in subjects:
        vec.append(m)
        depth = 2
        if m == "физика":
            make_buttons(message, "Выбери олимпиаду:", phisic_olimpiads)
    else:
        bot.send_message(message.chat.id, "Я сломался на 1 шаге \nНапиши '/start', чтобы починить меня!")

def Two(message):
    global vec
    global depth
    m = message.text.lower()
    if m in phisic_olimpiads:
        vec.append(m)
        depth = 3
        make_buttons(message, "Выбери класс", grades)
    else:
        bot.send_message(message.chat.id, "Я сломался на 2 шаге \nНапиши '/start', чтобы починить меня!")

def Three(message):
    global vec
    global depth
    m = message.text.lower()
    if m in grades:
        vec.append(m)
        depth = 4
        make_buttons(message, "Выбери год", years)
    else:
        bot.send_message(message.chat.id, "Я сломался на 3 шаге \nНапиши '/start', чтобы починить меня!")

def Four(message):
    global path
    global vec
    global depth
    m = message.text.lower()
    if m in years:
        vec.append(m)
        current_dir = make_path()
        for file in os.listdir(current_dir):
            bot.send_document(message.chat.id, open(current_dir + "/" + file,'rb'))
        vec.pop()
    else:
        bot.send_message(message.chat.id, "Я сломался на 4 шаге \nНапиши '/start', чтобы починить меня!")



@bot.message_handler(content_types=['text'])
def handle_text(message):
    global depth
    OpenToRead(message.chat.id)
    if message.text == "назад":
        Back(message)
    elif depth == 0:
        Zero(message)
    elif depth == 1:
        One(message)
    elif depth == 2:
        Two(message)
    elif depth == 3:
        Three(message)
    elif depth == 4:
        Four(message)
    OpenToWrite(message.chat.id)

# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#     bot.send_message(message.chat.id, type(message))

bot.polling(none_stop=True, interval=0)