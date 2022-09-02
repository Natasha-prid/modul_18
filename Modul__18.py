import telebot

from extensions import APIException, BotExtensions
from config import TOKEN


bot = telebot.TeleBot(TOKEN)

# Обрабатываются сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.chat.username}! Я Бот-Конвертер валют.\n\n"
                                      f"Чтобы узнать стоимость, введите команду в следующем формате:\n"
                                      f"<имя валюты цену которой нужно узнать> <имя валюты в которой надо узнать цену> <количество валюты> ( например EUR RUB 50 )\n"
                                      f"Допускается не указывать количество (пример USD RUB)\n\n"
                                      f"список доступных валют можно узнать по команде /values")



@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    bot.send_message(message.chat.id, BotExtensions.get_values())


# Обрабатываются все текстовые сообщения
@bot.message_handler(content_types=['text'])
def try_convert(message: telebot.types.Message):
    try:
        reply = BotExtensions.data_validation(message.text)

    except APIException as a:
        bot.send_message(message.chat.id, f'Ошибка пользователя:\n{a}\n')

    except Exception as a:
        bot.send_message(message.chat.id, f'Что-то пошло не так:\n{a}\n'
                                          f'Для помощи используйте команду /help')

    else:
        bot.send_message(message.chat.id, reply)


bot.polling()