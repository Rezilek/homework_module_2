import pytest

from typing import List, Dict, Any
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


# Фикстуры для тестов карт
@pytest.fixture
def valid_card_numbers() -> List[int]:
    return [1234567890123456, 1111222233334444, 9999999999999999]


@pytest.fixture
def invalid_card_numbers() -> List[tuple]:
    return [
        (123, ValueError),  # Слишком короткий номер
        ("abc", TypeError),  # Не число
        (None, TypeError),  # None значение
    ]


# Фикстуры для тестов счетов
@pytest.fixture
def valid_account_numbers() -> List[int]:
    return [1234567890, 9876543210, 9999999999]


@pytest.fixture
def invalid_account_numbers() -> List[tuple]:
    return [
        (123, ValueError),  # Слишком короткий номер
        ("xyz", TypeError),  # Не число
        (None, TypeError),  # None значение
    ]


# Тесты для get_mask_card_number
@pytest.mark.parametrize(
    "card_number, expected",
    [
        (1234567890123456, "1234 56** **** 3456"),
        (1111222233334444, "1111 22** **** 4444"),
        (9999999999999999, "9999 99** **** 9999"),
    ],
)
def test_get_mask_card_number_valid(card_number: int, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "card_number, expected_exception",
    [
        (123, ValueError),  # Слишком короткий номер
        ("abc", TypeError),  # Не число
        (None, TypeError),  # None значение
    ],
)
def test_get_mask_card_number_invalid(card_number: Any, expected_exception: type) -> None:
    with pytest.raises(expected_exception):
        get_mask_card_number(card_number)


# Тесты для get_mask_account
@pytest.mark.parametrize(
    "account_number, expected",
    [
        (1234567890, "**7890"),
        (9876543210, "**3210"),
        (9999999999, "**9999"),
    ],
)
def test_get_mask_account_valid(account_number: int, expected: str) -> None:
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "account_number, expected_exception",
    [
        (123, ValueError),  # Слишком короткий номер
        ("xyz", TypeError),  # Не число
        (None, TypeError),  # None значение
    ],
)
def test_get_mask_account_invalid(account_number: Any, expected_exception: type) -> None:
    with pytest.raises(expected_exception):
        get_mask_account(account_number)


# Тесты для mask_account_card
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card_valid(input_str: str, expected: str) -> None:
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize(
    "input_str, expected_error",
    [
        (123, TypeError),  # Число вместо строки
        (None, TypeError),  # None вместо строки
        ("Invalid", ValueError),  # Неверный формат
        ("Счет 123", ValueError),  # Слишком короткий номер счета
        ("Card 123", ValueError),  # Слишком короткий номер карты
    ],
)
def test_mask_account_card_invalid(input_str: Any, expected_error: type) -> None:
    with pytest.raises(expected_error):
        mask_account_card(input_str)


def test_mask_account_card_empty_string() -> None:
    with pytest.raises(ValueError, match="Входная строка не может быть пустой"):
        mask_account_card("")


# Тесты для get_date
@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-03-11T12:00:00", "11.03.2024"),
        ("2025-12-31T23:59:59", "31.12.2025"),
    ],
)
def test_get_date_valid(date_string: str, expected: str) -> None:
    assert get_date(date_string) == expected


@pytest.mark.parametrize(
    "invalid_input, expected_exception",
    [
        ("2024-03-11", ValueError),  # Нет времени
        ("11.03.2024", ValueError),  # Не ISO-формат
        ("invalid-date", ValueError),  # Некорректная строка
        (1234567890, TypeError),  # Число вместо строки
        (None, TypeError),  # None вместо строки
    ],
)
def test_get_date_invalid(invalid_input: Any, expected_exception: type) -> None:
    with pytest.raises(expected_exception):
        get_date(invalid_input)


# Фикстуры с тестовыми данными
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T12:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-10T12:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-20T12:00:00"},
        {"id": 4, "state": "PENDING", "date": "2023-01-05T12:00:00"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-01T12:00:00"},
    ]


# Тесты для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(sample_transactions: List[Dict[str, Any]], state: str, expected_ids: List[int]) -> None:
    filtered = filter_by_state(sample_transactions, state)
    assert [t["id"] for t in filtered] == expected_ids


def test_filter_by_state_default(sample_transactions: List[Dict[str, Any]]) -> None:
    filtered = filter_by_state(sample_transactions)
    assert [t["id"] for t in filtered] == [1, 3, 5]


# Тесты для sort_by_date
@pytest.mark.parametrize(
    "reverse, expected_order",
    [
        (True, [3, 1, 2, 4, 5]),  # По убыванию (новые сначала)
        (False, [5, 4, 2, 1, 3]),  # По возрастанию (старые сначала)
    ],
)
def test_sort_by_date(sample_transactions: List[Dict[str, Any]], reverse: bool, expected_order: List[int]) -> None:
    sorted_trans = sort_by_date(sample_transactions, reverse)
    assert [t["id"] for t in sorted_trans] == expected_order


def test_sort_by_date_default(sample_transactions: List[Dict[str, Any]]) -> None:
    sorted_trans = sort_by_date(sample_transactions)
    assert [t["id"] for t in sorted_trans] == [3, 1, 2, 4, 5]


# Тесты на граничные случаи
def test_empty_input() -> None:
    assert filter_by_state([]) == []
    assert sort_by_date([]) == []


def test_missing_state_field() -> None:
    transactions = [{"id": 1, "date": "2023-01-01T12:00:00"}]
    assert filter_by_state(transactions, "EXECUTED") == []


def test_missing_date_field() -> None:
    transactions = [{"id": 1, "state": "EXECUTED"}]
    with pytest.raises(KeyError):
        sort_by_date(transactions)


# Тест для проверки стабильности сортировки
def test_sort_stability() -> None:
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T12:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-15T12:00:00"},
    ]
    sorted_trans = sort_by_date(transactions)
    assert [t["id"] for t in sorted_trans] == [1, 2]  # Сохраняем исходный порядок
