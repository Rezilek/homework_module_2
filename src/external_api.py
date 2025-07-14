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
        transaction: Словарь с данными о транзакции.

    Returns:
        Сумма транзакции в рублях (float).

    Raises:
        ValueError: Если валюта транзакции не поддерживается.
        ConnectionError: Если не удалось получить курс валют.
    """
    try:
        amount = float(transaction["amount"])
    except (KeyError, ValueError) as e:
        raise ValueError("Invalid transaction amount") from e

    currency = transaction.get("currency")

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        raise ValueError(f"Unsupported currency: {currency}")

    try:
        response = requests.get(
            BASE_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": API_KEY}, timeout=10
        )
        response.raise_for_status()
        rates = response.json().get("rates", {})
        rate = rates.get("RUB")
        if rate is None:
            raise ConnectionError("RUB rate not found in response")
        return float(amount * rate)
    except requests.RequestException as e:
        raise ConnectionError("Failed to get exchange rate: {str(e)}") from e
