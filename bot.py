import telebot
from config import TOKEN
from extensions import CurrencyConverter, APIException, CURRENCIES

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Чтобы узнать цену валюты, отправьте сообщение в формате:\n"
        "<валюта которую хотите продать> <валюта которую хотите купить> <количество>\n"
        "Пример: доллар рубль 100\n\n"
        "Доступные валюты: /values"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:\n"
    for name in CURRENCIES:
        text += f"- {name}\n"
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        parts = message.text.strip().lower().split()

        if len(parts) != 3:
            raise APIException("Неверный формат запроса. Нужно три параметра.")

        base_name, quote_name, amount = parts

        if base_name not in CURRENCIES:
            raise APIException(f"Валюта {base_name} не поддерживается.")
        if quote_name not in CURRENCIES:
            raise APIException(f"Валюта {quote_name} не поддерживается.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество: {amount}")

        base = CURRENCIES[base_name]
        quote = CURRENCIES[quote_name]

        result = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        text = f"{amount} {base_name} = {result} {quote_name}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)