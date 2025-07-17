from src.log_config import setup_logger

# Настройка логера для модуля masks
logger = setup_logger('masks_module', 'masks.log')


def get_mask_card_number(card_number: int) -> str:
    """Возвращает замаскированную версию номера карты."""
    try:
        if not isinstance(card_number, int):
            raise TypeError("Номер карты должен быть целым числом")

        card_str = str(card_number)
        if len(card_str) < 16:
            raise ValueError("Номер карты должен содержать минимум 16 цифр")

        masked = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
        logger.debug(f"Успешная маскировка карты: {card_number} -> {masked}")
        return masked

    except (TypeError, ValueError) as e:
        logger.error(f"Ошибка маскировки карты {card_number}: {str(e)}", exc_info=True)
        raise


def get_mask_account(account_number: int) -> str:
    """Возвращает замаскированную версию номера счёта."""
    try:
        if not isinstance(account_number, int):
            raise TypeError("Номер счёта должен быть целым числом")

        account_str = str(account_number)
        if len(account_str) < 4:
            raise ValueError("Номер счёта должен содержать минимум 4 цифры")

        masked = f"**{account_str[-4:]}"
        logger.debug(f"Успешная маскировка счёта: {account_number} -> {masked}")
        return masked

    except (TypeError, ValueError) as e:
        logger.error(f"Ошибка маскировки счёта {account_number}: {str(e)}", exc_info=True)
        raise


if __name__ == '__main__':
    # Демонстрация работы функций с логированием
    print("Демонстрация работы masks.py:")
    try:
        # Успешные случаи
        print(get_mask_card_number(1234567890123456))  # -> "1234 56** **** 3456"
        print(get_mask_account(12345678))  # -> "**5678"

        # Ошибочные случаи (для демонстрации логирования)
        print(get_mask_card_number("text"))  # TypeError
        print(get_mask_card_number(12345))  # ValueError (слишком короткий)
        print(get_mask_account(12))  # ValueError
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    print("Проверьте логи в logs/masks.log")