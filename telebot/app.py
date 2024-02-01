import telebot
from config import TOKEN, keys, headers, payload
from extentions import CryptoConvertor, ConvertionExeption

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n <Имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Увидеть список всех доступных валют можно при помощи команды /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text ='\n'.join((text, key, ))
    bot.reply_to(message,text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertionExeption('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConvertor.convert(quote, base, amount, headers, payload)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
