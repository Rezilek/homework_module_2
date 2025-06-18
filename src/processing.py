from typing import Dict, List  # Импортирование необходимых типов


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
