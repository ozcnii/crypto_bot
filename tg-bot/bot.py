from telebot import TeleBot, types
import requests
import json
from config import DevelopmentConfig

bot = TeleBot(token=DevelopmentConfig.TOKEN)
HOST = DevelopmentConfig.HOST

@bot.message_handler(commands=['start'])
def listen(message: types.Message):
    #Кнопка перейти
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Перейти', web_app=types.WebAppInfo(DevelopmentConfig.WEBAPP_URL)))
    
    #Отправка сообщения
    bot.send_message(chat_id=message.chat.id, text='Добро пожаловать!', 
                    reply_markup=kb)

    #Регистрация пользователя
    requests.post(
        #Ссылка
        url=f"{HOST}/users",
        
        #Заголовки
        headers={
            'Content-Type': 'application/json'
        },
        
        #Контент
        data=json.dumps({
            "chat_id":message.chat.id,
            "username":message.from_user.username,
            "balance":1000,
            "league":"bronze",
            "boosters":[0,0,0,0,0],
        })
    )

bot.infinity_polling()