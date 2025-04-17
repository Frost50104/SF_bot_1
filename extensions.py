import requests
import json
from config import ACCESS_KEY

class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        url = f"https://api.exchangerate.host/convert"
        params = {
            'from': base.upper(),
            'to': quote.upper(),
            'amount': amount,
            'access_key': ACCESS_KEY
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise APIException(f"Ошибка запроса к API. Код ответа: {response.status_code}")

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise APIException("Ошибка обработки ответа от API.")

        if not data.get('success', False):
            raise APIException(f"Ошибка при запросе валюты: {data}")

        result = data.get('result')
        if result is None:
            raise APIException("Не найден результат конвертации.")

        return round(result, 4)


CURRENCIES = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}