import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
BASE_URL = 'https://api.apilayer.com/exchangerates_data/latest'


def convert_to_rub(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Сумма в рублях или None при ошибке
    """
    try:
        amount = float(transaction['amount'])
        currency = transaction['currency']

        if currency == 'RUB':
            return amount

        if currency in ('USD', 'EUR'):
            response = requests.get(
                BASE_URL,
                params={'base': currency, 'symbols': 'RUB'},
                headers={'apikey': API_KEY}
            )
            response.raise_for_status()
            rate = response.json()['rates']['RUB']
            return round(amount * rate, 2)

        return None
    except (KeyError, requests.RequestException, ValueError):
        return None

