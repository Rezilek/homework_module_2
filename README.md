# Банковские транзакции - утилиты для обработки и тестирование

## Описание проекта

Проект предоставляет комплексное решение для работы с банковскими транзакциями, включая:
- Маскировку конфиденциальных данных (карты, счета)
- Фильтрацию и сортировку транзакций
- Генерацию тестовых данных
- Логирование операций
- Полный набор модульных тестов

## Структура проекта

```
project/
├── src/
│   ├── __init__.py
│   ├── decorators.py      # Модуль логирования операций
│   ├── generators.py      # Генераторы тестовых данных
│   ├── masks.py           # Функции маскировки данных
│   ├── processing.py      # Обработка транзакций
│   ├── utils.py           # Вспомогательные утилиты
│   ├── widget.py          # Основные функции интерфейса
│   └── external_api.py    # Работа с внешними API
├── tests/
│   ├── __init__.py
│   ├── test_decorators.py
│   ├── test_external_api.py
│   ├── test_generators.py
│   ├── test_modul.py
│   └── test_utils.py
├── data/
│   └── operations.json    # Пример данных транзакций
├── .env.template          # Шаблон для переменных окружения
├── requirements.txt       # Зависимости Python
├── pyproject.toml         # Конфигурация проекта
└── README.md
```

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Rezilek/homework_module_2.git
   cd homework_module_2
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Настройте окружение:
   ```bash
   poetry install
   poetry shell
   cp .env.template .env
   ```
     
   Затем откройте `.env` и укажите ваш ключ от [Exchange Rates API](https://apilayer.com/marketplace/exchangerates_data-api):
   ```ini
   EXCHANGE_RATE_API_KEY=ваш_ключ_здесь
   
4. Убедитесь в наличии Python 3.8+:
   ```bash
   python --version
   ```

## Основной функционал

### Модуль masks.py

Функции для маскировки конфиденциальных данных:

```python
from src.masks import get_mask_card_number, get_mask_account

# Маскировка номера карты
print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361

# Маскировка номера счета
print(get_mask_account("73654108430135874305"))  # **4305
```

**Тесты:**
- Проверка корректности маскирования
- Обработка невалидных данных
- Проверка граничных значений

### Модуль widget.py

Утилиты для работы с интерфейсом:

```python
from src.widget import mask_account_card, get_date

# Автоматическая маскировка
print(mask_account_card("Visa Platinum 7000792289606361"))

# Форматирование даты
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
```

### Модуль processing.py

Обработка транзакций:

```python
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    # ... другие транзакции
]

# Фильтрация по статусу
executed = filter_by_state(transactions, "EXECUTED")

# Сортировка по дате
sorted_trans = sort_by_date(transactions, reverse=True)
```

### Модуль generators.py

Генерация тестовых данных:

```python
from src.generators import card_number_generator, filter_by_currency

# Генерация номеров карт
for card in card_number_generator(1, 5):
    print(card)  # 0000 0000 0000 0001, ..., 0000 0000 0000 0005

# Фильтрация транзакций по валюте
usd_transactions = filter_by_currency(transactions, "USD")
```

### Модуль decorators.py

Логирование операций:

```python
from src.decorators import log

@log(filename="operations.log")
def transfer(amount: float, from_acc: str, to_acc: str) -> bool:
    """Выполняет перевод средств между счетами"""
    # Логика перевода
    return True

transfer(1000.0, "Счет 1234", "Счет 5678")
```

### Модуль external_api.py

Конвертация валютных транзакций в рубли через внешний API:

```python
from src.external_api import convert_transaction_amount

transaction = {
    "operationAmount": {
        "amount": "100",
        "currency": {
            "code": "USD"
        }
    }
}

# Конвертация USD → RUB по текущему курсу
converted_amount = convert_transaction_amount(transaction)
print(converted_amount)  # Пример: 7500.50 (100 USD * 75.005)
```

**Особенности:**
- Поддерживает валюты: `USD`, `EUR`, `RUB`
- Данные должны содержать поля:  
  `operationAmount.amount` (число)  
  `operationAmount.currency.code` (код валюты)
- В случае ошибки возвращает `None` и пишет в лог
- 
## Тестирование

**Проверка конвертации валют:**
- Корректное извлечение суммы и кода валюты из `operationAmount`
- Обработка транзакций без нужных полей (`KeyError`)
- Конвертация RUB → RUB (без вызова API)
- Мокирование запросов к API в тестах

Запуск всех тестов:
```bash
pytest -v tests/ --cov=src --cov-report=html
```

Проверка стиля и типов:
```bash
flake8 src/
mypy src/ tests/
```

**Требования к покрытию:**
- 100% для основных функций
- Тестирование граничных случаев
- Проверка обработки ошибок
- - 100% coverage для `external_api.py`, включая:
  - Обработку правильной структуры транзакции
  - Ошибки подключения к API
  - Некорректные коды валют

## Документация

Полная документация доступна в docstrings модулей:
- `masks.py` - маскировка данных
- `widget.py` - функции интерфейса
- `processing.py` - обработка транзакций
- `generators.py` - генерация данных
- `decorators.py` - система логирования

## Лицензия

Проект распространяется под лицензией MIT.

## Контакты

**Автор:** Резиля Столярова  
**Email:** rezilek5177@gmail.com  
**GitHub:** [Rezilek](https://github.com/Rezilek)