import requests
import json
from config import keys

class ConvertionExeption(Exception):
    pass

class CryptoConvertor:
    @staticmethod
    def convert(quote: str, base: str, amount: str, headers, payload):

        if quote == base:
            raise ConvertionExeption(f'Невозможно перевести одинаковые валюты {base}.')
        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Неудалось обработать валюту {quote}')

        try:
            base_tiker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Неудалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Не удалось обработать количество {amount}')

        r = requests.request('get',url=f"https://api.apilayer.com/exchangerates_data/latest?symbols={base_tiker}&base={quote_tiker}",headers=headers, data=payload)
        prise = json.loads(r.text)['rates'][keys[base]]
        total_base = str(float(amount)*prise)

        return total_base