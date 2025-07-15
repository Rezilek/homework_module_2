import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_transaction_amount(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции (должен содержать operationAmount)

    Returns:
        Сумма транзакции в рублях (float)

    Raises:
        ValueError: Если валюта транзакции не поддерживается или данные некорректны
        ConnectionError: Если не удалось получить курс валют
    """
    try:
        # Получаем данные из правильной структуры
        amount_data = transaction["operationAmount"]
        amount = float(amount_data["amount"])
        currency = amount_data["currency"]["code"]

        if currency == "RUB":
            return amount

        if currency not in ("USD", "EUR"):
            raise ValueError(f"Unsupported currency: {currency}")

        try:
            response = requests.get(
                BASE_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": API_KEY}, timeout=5
            )
            response.raise_for_status()
            rate = response.json()["rates"]["RUB"]
            return amount * rate

        except (requests.RequestException, KeyError) as e:
            raise ConnectionError(f"API request failed: {str(e)}")

    except (KeyError, ValueError) as e:
        raise ValueError(f"Invalid transaction data: {str(e)}")
