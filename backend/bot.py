from telebot import TeleBot, types
import requests
import json
from config import DevelopmentConfig

bot = TeleBot(token=DevelopmentConfig.TOKEN)
HOST = DevelopmentConfig.HOST

print("@Aboba")
@bot.message_handler(commands=['start'])
def listen(message: types.Message):
    #Кнопка перейти
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Перейти', web_app=types.WebAppInfo('https://cepbep4-airvapebot-b471.twc1.net')))
        
    #Отправка сообщения
    bot.send_message(
        chat_id=message.chat.id,
        text='Добро пожаловать!', 
        #reply_markup=kb
    )

    premium = 1 if message.from_user.is_premium else 0

    #Регистрация пользователя
    requests.post(
        #Ссылка
        url=f"{HOST}/users",
        
        #Заголовки
        headers={
            'Content-Type': 'application/json',
            "Authorization": f'Bearer {DevelopmentConfig.TELEGRAM_BOT_AUTH_TOKEN}'
        },
        
        #Контент
        data=json.dumps({
            "chat_id":message.chat.id,
            "username":message.from_user.username,
            "premium":premium,
            "balance":1000,
            "league":"bronze",
            "boosters":[0,0,0,0,0],
        })
    )
    
    #Добавление реферала
    if len(message.text.split()) != 1:
        requests.post(
            #Ссылка
            url=f"{HOST}/users/addref",
            
            #Заголовки
            headers={
                'Content-Type': 'application/json',
                "Authorization": f'Bearer {DevelopmentConfig.TELEGRAM_BOT_AUTH_TOKEN}'
            },
            
            #Контент
            data=json.dumps({
                "ref_id":message.chat.id,
                "admin_chat_id":message.text.split()[1],
                "premium":message.from_user.is_premium
            })
        )

bot.infinity_polling()