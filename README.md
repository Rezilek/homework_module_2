# Банковские транзакции - утилиты для обработки

## Описание проекта

Этот проект предоставляет набор утилит для работы с банковскими транзакциями, включая:
- Фильтрацию и сортировку транзакций
- Маскировку номеров карт и счетов
- Форматирование дат

## Структура проекта
```
src/
├── masks.py
├── processing.py
├── widget.py
```

## Установка

1. Склонируйте репозиторий:

git clone git@github.com:Rezilek/homework_10_1.git

2. Убедитесь, что у вас установлен Python 3.6 или выше:

python --version

## Функционал

### masks.py

1. **`get_mask_card_number(card_number: int) -> str`**  
   Возвращает замаскированный номер кредитной карты в формате `XXXX XX** **** XXXX`.

2. **`get_mask_account(account_number: int) -> str`**  
   Возвращает замаскированный номер счета в формате `**XXXX`.

### widget.py

1. **`mask_account_card(input_str: str) -> str`**  
   Маскирует номер карты или счета в зависимости от типа, указанного во входной строке.

2. **`get_date(date_string: str) -> str`**  
   Преобразует дату из формата ISO в формат `ДД.ММ.ГГГГ`.

### processing.py

1. **`filter_by_state(transactions: List[Dict], state: str = 'EXECUTED') -> List[Dict]`**  
   Фильтрует транзакции по состоянию (по умолчанию - 'EXECUTED').

2. **`sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]`**  
   Сортирует транзакции по дате (по умолчанию - по убыванию).

## Примеры использования

```python
# Пример работы с маскировкой
print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361
print(mask_account_card("Счет 73654108430135874305"))       # Счет **4305

# Пример работы с датами
print(get_date("2024-03-11T02:26:18.671407"))              # 11.03.2024

# Пример работы с транзакциями
transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

print(filter_by_state(transactions))  # Фильтрация по EXECUTED
print(sort_by_date(transactions))    # Сортировка по дате (по убыванию)
```

## Использование

### Маскировка данных
```python
from src.widget import mask_account_card

print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361
print(mask_account_card("Счет 73654108430135874305"))       # Счет **4305
```

### Работа с датами
```python
from src.widget import get_date

print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
```

### Обработка транзакций
```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    # ... другие транзакции
]

# Фильтрация выполненных транзакций
executed = filter_by_state(transactions)

# Сортировка по дате (новые сначала)
sorted_trans = sort_by_date(transactions)
```

## Документация

Полная документация по API доступна в исходных файлах:
- `src/masks.py` - маскировка номеров
- `src/widget.py` - основные функции интерфейса
- `src/processing.py` - обработка транзакций

## Лицензия

Этот проект распространяется под лицензией MIT.

```
Copyright (c) 2025 Rezilek

## Автор

Резиля Столярова 
Email: rezilek5177@gmail.com  
GitHub: [Rezilek](https://github.com/Rezilek)

