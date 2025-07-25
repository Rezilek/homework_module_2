import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Фильтрует транзакции по состоянию.

    Параметры:
    транзакции (List[Dict]): список транзакций для фильтрации.
    state (str): состояние для фильтрации (по умолчанию - 'ИСПОЛНЕНО').

    Возврат:
    List[Dict]: Список транзакций, соответствующих состоянию.
    """
    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортировка транзакций по дате.

    Параметры:
    транзакции (List[Dict]): список транзакций для сортировки.
    reverse (bool): порядок сортировки; True - по убыванию, False - по возрастанию (default is True).

    Возврат:
    List[Dict]: отсортированный список транзакций.
    """
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых встречается заданная строка (с использованием регулярных выражений).

    :param data: Список транзакций (словарей)
    :param search: Строка для поиска
    :return: Отфильтрованный список транзакций
    """
    pattern = re.compile(search, re.IGNORECASE)
    result = []
    for transaction in data:
        description = transaction.get("description", "")
        if description and pattern.search(description):
            result.append(transaction)
    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций в указанных категориях.

    :param data: Список транзакций (словарей)
    :param categories: Список категорий для подсчета
    :return: Словарь с количеством операций по категориям
    """
    descriptions = []
    for t in data:
        desc = t.get("description")
        if desc is not None and desc in categories:
            descriptions.append(desc)
    return dict(Counter(descriptions))


# Пример использования
if __name__ == "__main__":
    transactions = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    print(filter_by_state(transactions))  # Пример использования фильтрации
    print(sort_by_date(transactions))  # Пример использования сортировки
