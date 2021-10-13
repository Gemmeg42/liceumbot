# -*- coding: utf-8 -*-
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
from telegram import ReplyKeyboardMarkup
import random
import sqlite3

TOKEN = 'Засекречено от Дани'
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
mod = random.choice(['quiz2.csv', 'quiz1.csv'])

f = open(mod, 'r')
a = f.read()
a = a.split(';')
i = 0
score = 0
s = -1
ranked = False


def start(update, context):
    global i
    global score 
    global ranked
    ranked = False
    i = 0
    score = 0    
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Добро пожаловать на квиз!")
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Вам нужно будет ответить на 10 вопросов") 
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="За каждый правильный ответ вы получаете 10 баллов")
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="введите /rank если хотите сохранить счет")    
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Чтобы перейти на следующий вопрос используйте команду /next")
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Если вам не засчитали правильный ответ, введите команду /yes")
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Удачи!")  
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Первый вопрос:")
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=a[0])    


def echo(update, context):
    global i
    global score
    global ranked
    text = '"' + update.message.text 
    if i % 2 == 1:
        return
    i += 1
    if text.upper() == a[i].upper():
        score += 10
        s = score
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text='Верно!')    
        reply_keyboard = [['/next', '/yes']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True) 
        update.message.reply_text('Ваш счет:' + str(s), reply_markup=markup)            
    else:
        s = score
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text='Неверно. Правильный ответ:')
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text=a[i][1:len(a[i]) + 1]) 
        reply_keyboard = [['/next', '/yes']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False) 
        update.message.reply_text('Ваш счет:' + str(s), reply_markup=markup)        


def next(update, context): 
    global i
    global ranked
    i += 1
    if i > 19:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text='Квиз закончен')        
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text='Спасибо за игру!')
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text='Ваш счет: ' + str(score))
        if ranked:
            context.bot.send_message(chat_id=update.effective_chat.id, 
                                     text="Введите команду /save для сохранения\
                                     результата")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text=a[i])  


def yes(update, context):
    global s
    global score
    if s != i:
        score += 10
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text='Хорошо')    
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text='Ваш счет: ' + str(score))
        s = i
        
        
def rank(update, context):
    global ranked
    ranked = True


def save(update, context):
    global score
    global ranked
    if ranked:
        bd = 'score.bd'
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text=str(score))
        con = sqlite3.connect(bd)
        cur = con.cursor()
        text = update.message.text 
        cur.execute("insert into score(points) values(" + str(score) + ")")
        con.commit()    


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)    

yes_handler = CommandHandler('yes', yes)
dispatcher.add_handler(yes_handler) 

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

save_handler = CommandHandler('save', save)
dispatcher.add_handler(save_handler)

next_handler = CommandHandler('next', next)
dispatcher.add_handler(next_handler)

rank_handler = CommandHandler('rank', rank)
dispatcher.add_handler(rank_handler)

updater.start_polling()
updater.idle()
