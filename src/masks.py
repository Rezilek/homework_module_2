def get_mask_card_number(card_number: int) -> str:
    """
    Возвращает замаскированную версию номера кредитной карты в формате XXXX XX** **** XXXX.
    Выбрасывает ValueError, если номер карты слишком короткий.
    """
    if not isinstance(card_number, int):
        raise TypeError("Номер карты должен быть целым числом")

    card_string = str(card_number)
    if len(card_string) < 16:
        raise ValueError("Номер карты должен содержать минимум 16 цифр")

    return f"{card_string[:4]} {card_string[4:6]}** **** {card_string[-4:]}"


def get_mask_account(account_number: int) -> str:
    """
    Возвращает замаскированную версию номера счета в формате **XXXX.
    Выбрасывает ValueError, если номер счёта слишком короткий.
    """
    if not isinstance(account_number, int):
        raise TypeError("Номер счёта должен быть целым числом")

    account_string = str(account_number)
    if len(account_string) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")

    return f"**{account_string[-4:]}"
