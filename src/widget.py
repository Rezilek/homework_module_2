# src/widget.py
from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime

def mask_account_card(input_str: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа, указанного при вводе"""
    if not isinstance(input_str, str):
        raise TypeError("Ожидается строка в формате 'Тип Номер'")

    if not input_str.strip():
        raise ValueError("Входная строка не может быть пустой")

    parts = input_str.split()
    if len(parts) < 2:
        raise ValueError("Неверный формат входных данных. Ожидается 'Тип Номер'")

    type_identifier = " ".join(parts[:-1])
    number = parts[-1]

    if "Счет" in type_identifier:
        return f"{type_identifier} {get_mask_account(int(number))}"
    else:
        return f"{type_identifier} {get_mask_card_number(int(number))}"


def get_date(date_string: str) -> str:
    """Преобразует дату из полного ISO формата (с временем) в формат ДД.ММ.ГГГГ.
    Выбрасывает:
    - TypeError если входные данные не строка
    - ValueError если:
      - Нет времени (отсутствует 'T')
      - Неправильный формат даты
    """
    if not isinstance(date_string, str):
        raise TypeError("Ожидается строка с датой в формате ISO")

    if "T" not in date_string:
        raise ValueError("Дата должна быть в полном ISO-формате (YYYY-MM-DDTHH:MM:SS)")

    try:
        date = datetime.fromisoformat(date_string)
        return date.strftime("%d.%m.%Y")
    except ValueError as e:
        raise ValueError(f"Неверный формат даты: {e}")

if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))  # Проверка маскировки карты
    print(mask_account_card("Счет 73654108430135874305"))  # Проверка маскировки счета
    print(get_date("2024-03-11T02:26:18.671407"))  # Преобразование даты