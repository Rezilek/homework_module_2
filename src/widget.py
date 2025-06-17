# src/widget.py
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_str: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа, указанного при вводе"""
    parts = input_str.split(" ")  # Разделяет строку ввода
    type_identifier = " ".join(parts[:-1])  # Все части, кроме последней для данного типа
    number = parts[-1]  # Последняя часть - это число

    # Определяет, относится ли идентификатор к карте или счету
    if "Счет" in type_identifier:
        return f"{type_identifier} {get_mask_account(int(number))}"  # Маскирует счет
    else:
        return f"{type_identifier} {get_mask_card_number(int(number))}"  # Маскирует карту


def get_date(date_string: str) -> str:
    """Преобразует дату из формата ISO в формат  ДД.ММ.ГГГГ."""
    from datetime import datetime  # Импорт datetime для манипулирования датой

    date = datetime.fromisoformat(date_string)  # Разбор ISO формата
    return date.strftime("%d.%m.%Y")  # Форматирование в ДД.ММ.ГГГГ.


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))  # Проверка маскировки карты
    print(mask_account_card("Счет 73654108430135874305"))  # Проверка маскировки счета
    print(get_date("2024-03-11T02:26:18.671407"))  # Преобразование даты
