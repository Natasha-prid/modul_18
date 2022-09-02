import requests
import json
from config import currency, url

# исключения при вводе пользователя
class APIException(Exception):
    pass

# класс с методами бота
class BotExtensions:

    # вывод в сообщение текста доступных валют
    @staticmethod
    def get_values():

        reply = "Доступные валюты (допускается ввод в произвольном регистре):\n"
        for L in currency.values():
            reply += '\n' + '\t' + ' - '.join(L)

        return(reply)


    # проверки данных от пользователя, обработка исключений и вывод текста
    @staticmethod
    def data_validation(values: str):

        txt = f'\nВведите команду в следующем формате:\n ' \
                f'<имя валюты цену которой нужно узнать> <имя валюты в которой надо узнать цену> <количество валюты> (USD RUB 1000)\n' \
                f'Допускается не указывать количество (USD RUB)\n\n' \
                f'список доступных валют можно узнать по команде /values'

        values = values.split()

        if len(values) < 2:
            raise APIException(f'"Параметров должно быть не менее двух"\n'
                               f'Например USD EUR')
        elif len(values) > 3:
            raise APIException(f'"Параметров слишком много"' + txt)

        elif len(values) == 2:
            values += '1'

        quote, base, amount = values

        quote_r, base_r = '', ''

        for k, v in currency.items():

            if quote.upper() in v:
                quote_r = k

            if base.upper() in v:
                base_r = k

        if quote_r == '':
            raise APIException(f'"Не удалось обработать запрос {quote}"' + txt)

        if base_r == '':
            raise APIException(f'"Не удалось обработать запрос {base}"' + txt)

        if quote_r == base_r:
            raise APIException(f'"Введены одинаковые валюты {quote} {base}"' + txt)

        try:
            amount = abs(float(amount.replace(',', '.')))

        except:
            raise APIException(f'"Не удалось обработать количество {amount}"' + txt)

        total = BotExtensions.get_price(quote_r, base_r, amount)

        reply = f'{amount} {quote} = {round(total, 9)} {base}'

        return reply


    # возвращает нужную сумму в валюте
    @staticmethod
    def get_price(quote: str, base: str, amount: float):

        try:
            req = requests.get(url[0] + quote + url[1] + base)

        except:
            raise Exception(f'"Сервер не отвечает"\n'
                               f'Попробуйте повторить запрос позже.\n')

        try:
            total = json.loads(req.content)[base] * amount

        except:
            raise Exception(f'"Неожиданный ответа сервера: {json.loads(req.content)}"\n'
                               f'Попробуйте повторить запрос позже.\n')

        return total