# Банковские транзакции - утилиты для обработки и тестирование

## Описание проекта

Проект предоставляет комплексное решение для работы с банковскими транзакциями, включая:
- Маскировку конфиденциальных данных (карты, счета)
- Фильтрацию и сортировку транзакций
- Генерацию тестовых данных
- Логирование операций
- Работу с внешними API
- Полный набор модульных тестов

## Структура проекта

```
project/
├── src/
│   ├── __init__.py
│   ├── decorators.py       # Модуль логирования операций
│   ├── file_reader.py      # Новый модуль для CSV/Excel
│   ├── generators.py       # Генераторы тестовых данных
│   ├── masks.py            # Функции маскировки данных
│   ├── processing.py       # Обработка транзакций
│   ├── utils.py            # Вспомогательные утилиты
│   ├── widget.py           # Основные функции интерфейса
│   ├── external_api.py     # Работа с внешними API
│   └── log_config.py       # Настройка системы логирования
├   └── main.py             # 
── tests/
│   ├── __init__.py
│   ├── test_decorators.py
│   ├── test_external_api.py
│   ├── test_file_reader.py # Тесты для нового модуля
│   ├── test_generators.py
│   ├── test_modul.py       # Тесты основных функций
│   ├── test_utils.py       # Тесты утилит
│   └── test_logging.py     # Тесты логирования
├── data/
│   └── operations.json     # Пример данных транзакций
│   ├── transactions.csv    # Пример CSV файла
│   └── transactions.xlsx   # Пример Excel файла
├── logs/                   # Директория для логов
│   ├── file_reader.log       # Логи нового модуля
│   ├── masks.log
│   ├── utils.log
├── .env.template           # Шаблон для переменных окружения
├── requirements.txt        # Зависимости Python
├── pyproject.toml          # Конфигурация проекта
├── setup.py                  # Для корректных импортов
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
   ```

4. Убедитесь в наличии Python 3.8+:
   ```bash
   python --version
   ```

## Основной функционал

### Модуль masks.py

Функции для маскировки конфиденциальных данных с логированием в файл `logs/masks.log`:

```python
from src.masks import get_mask_card_number, get_mask_account

# Маскировка номера карты
print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361

# Маскировка номера счета
print(get_mask_account("73654108430135874305"))  # **4305
```

**Особенности:**
- Автоматическое создание директории logs/
- Детальное логирование успешных операций и ошибок
- Валидация входных данных

**Тесты:**
- Проверка корректности маскирования
- Обработка невалидных данных
- Проверка граничных значений
- Тестирование записей в логах

### Модуль utils.py

Утилиты для работы с файлами и данными:

```python
from src.utils import read_json_file

# Чтение JSON-файла с транзакциями
transactions = read_json_file("data/operations.json")
```

**Особенности:**
- Логирование операций в файл `logs/utils.log`
- Автоматическая обработка ошибок:
  - Файл не найден
  - Невалидный JSON
  - Отсутствие ожидаемой структуры данных
- Возврат пустого списка при ошибках

### Модуль widget.py

Утилиты для работы с интерфейсом:

```python
from src.widget import mask_account_card, get_date

# Автоматическая маскировка
print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361

# Форматирование даты
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
```

### Модуль processing.py

- `filter_by_state()` - фильтрация транзакций по статусу
- `sort_by_date()` - сортировка транзакций по дате
- `process_bank_search()` - поиск транзакций по описанию (регулярные выражения)
- `process_bank_operations()` - подсчет операций по категориям

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
### Модуль main.py

Реализует основной пользовательский интерфейс:
- Выбор источника данных (JSON/CSV/XLSX)
- Фильтрация по статусу операции
- Сортировка по дате
- Фильтрация по валюте
- Поиск по ключевым словам
- Форматированный вывод результатов

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
- Кэширование курсов валют
- Обработка ошибок подключения

### Модуль log_config.py

Централизованная настройка системы логирования:

```python
from src.log_config import setup_logger

# Инициализация логгера для модуля
logger = setup_logger('module_name', 'module.log')

# Пример использования
logger.debug("Отладочное сообщение")
logger.error("Ошибка обработки данных")
```

**Особенности:**
- Автоматическое создание директории logs/
- Форматирование записей логов
- Гибкая настройка уровня логирования
- UTF-8 кодировка логов

### Модуль file_reader.py

Поддержка чтения транзакций из CSV и Excel файлов.

#### Функции:
- `read_csv(file_path: str) -> list[dict]`: Читает CSV файл и возвращает список словарей.
- `read_excel(file_path: str) -> list[dict]`: Читает Excel файл (первый лист) и возвращает список словарей.

Пример использования:
```python
from src.file_reader import read_csv, read_excel

csv_transactions = read_csv("data/transactions.csv")
excel_transactions = read_excel("data/transactions.xlsx")
```

**Особенности:**
- Автоматическое преобразование NaN в None
- Поддержка разных кодировок CSV
- Гибкий выбор листов в Excel
## Тестирование

**Комплексное тестирование системы:**
- Модульные тесты всех компонентов
- Тесты обработки ошибок
- Проверка логирования операций
- Тесты граничных случаев

**Запуск всех тестов:**
```bash
pytest -v tests/ --cov=src --cov-report=html
```

**Проверка стиля и типов:**
```bash
flake8 src/
mypy src/ tests/
```

**Ключевые тест-кейсы:**
1. Тестирование маскировки данных:
   - Корректная маскировка карт и счетов
   - Обработка невалидных номеров
   - Проверка записей в логах

2. Тестирование работы с файлами:
   - Чтение валидного JSON
   - Обработка битых файлов
   - Чтение несуществующих файлов
   - Проверка логов при ошибках

3. Тестирование конвертации валют:
   - Корректное извлечение данных из транзакции
   - Обработка транзакций без нужных полей
   - Конвертация RUB → RUB (без вызова API)
   - Мокирование API-запросов

**Требования к покрытию:**
- 100% покрытие для основных функций
- 100% покрытие обработки ошибок
- Тестирование граничных случаев
- Валидация записей в логах

## Документация

Полная документация доступна в docstrings модулей:
- `masks.py` - маскировка данных с логированием
- `utils.py` - работа с файлами и JSON
- `widget.py` - функции интерфейса
- `processing.py` - обработка транзакций
- `generators.py` - генерация данных
- `decorators.py` - система логирования
- `external_api.py` - работа с внешними API
- `log_config.py` - настройка системы логирования

## Лицензия

Проект распространяется под лицензией MIT.

## Контакты

**Автор:** Резиля Столярова  
**Email:** rezilek5177@gmail.com  
**GitHub:** [Rezilek](https://github.com/Rezilek)
```