# Банковские транзакции - утилиты для обработки и тестирование

## Описание проекта

Проект предоставляет набор инструментов для работы с банковскими транзакциями, включая:
- Маскировку номеров карт и счетов
- Фильтрацию и сортировку транзакций
- Форматирование дат
- Полный набор тестов для всех функций

## Структура проекта

```
project/
├── src/
│   ├── __init__.py
|   ├── decorators.py   # Основной модуль с декоратором
|   |__ generators.py
│   ├── masks.py        # Функции маскировки
│   ├── processing.py   # Обработка транзакций
│   └── widget.py       # Вспомогательные функции
├── tests/
│   ├── __init__.py
|   ├── test_decorators.py # Тесты с аннотациями типов
│   └── test_generators.py # Новые тесты 
|   |__ test_modul.py      # Все тесты 
├── requirements.txt
└── README.md
```

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Rezilek/git@github.com:Rezilek/homework_module_2.git
   cd git@github.com:Rezilek/homework_module_2.git
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Установить poetry
   ```
   poetry install
   ```
4. Требования к окружению

 Активировать виртуальное окружение
   ```
   poetry shell
   ```
Зависимости:
  - pytest
  - pytest-cov
  - mypy (для проверки типов)

5. Убедитесь, что у вас установлен Python 3.8 или выше:
   ```bash
   python --version
   ```

## Функционал

### Module masks.py

1. `get_mask_card_number(card_number: int) -> str`  
   Возвращает замаскированный номер кредитной карты в формате `XXXX XX** **** XXXX`.

**Тесты:**
- Проверка корректного маскирования
- Проверка ошибок для невалидных данных:
  - Слишком короткий номер (ValueError)
  - Нечисловые данные (TypeError)
  - None значение (TypeError)

2. `get_mask_account(account_number: int) -> str`
   Возвращает замаскированный номер счета в формате `**XXXX`.

**Тесты:**
- Проверка корректного маскирования
- Проверка ошибок (аналогично картам)

3. `mask_account_card(input_str: str) -> str`
Автоматически определяет тип (карта/счет) и применяет соответствующую маскировку

**Тесты:**
- Проверка корректного определения типа
- Проверка обработки ошибок:
  - Неверный формат строки
  - Слишком короткие номера
  - Не строковые данные

### Module widget.py

1. `mask_account_card(input_str: str) -> str`
Автоматически определяет тип (карта/счет) и применяет соответствующую маскировку

**Тесты:**
- Проверка корректного определения типа
- Проверка обработки ошибок:
  - Неверный формат строки
  - Слишком короткие номера
  - Не строковые данные

2. `get_date(date_string: str) -> str`
Преобразует дату из ISO формата в `ДД.ММ.ГГГГ`

**Тесты:**
- Проверка корректного форматирования
- Проверка ошибок для:
  - Неполных дат (без времени)
  - Неправильного формата
  - Не строковых данных

### Module processing.py

1. `filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]`
# Фильтрует транзакции по состоянию (EXECUTED, CANCELED, PENDING)

**Тесты:**
- Фильтрация по каждому состоянию
- Проверка значения по умолчанию
- Обработка пустого списка
- Обработка транзакций без поля state

2. `sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]`
Сортирует транзакции по дате (по умолчанию - новые сначала)

**Тесты:**
- Проверка сортировки по возрастанию и убыванию
- Проверка стабильности сортировки
- Обработка транзакций без поля date
- Обработка пустого списка

#### Примеры использования

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

### Module generators.py

#### Фильтрация транзакций

1. `filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]`
Фильтрует транзакции по заданной валюте

**Тесты:**
- Корректная фильтрация по валюте USD/RUB
- Обработка пустого списка транзакций
- Обработка отсутствия заданной валюты
- Проверка типа возвращаемого значения (Iterator)

#### Получение описаний

2. `transaction_descriptions(transactions: List[Dict]) -> Iterator[str]`
Извлекает описания транзакций

**Тесты:**
- Корректное извлечение описаний
- Обработка транзакций без поля description
- Обработка пустого списка транзакций
- Проверка порядка вывода описаний

#### Генерация номеров карт

3. `card_number_generator(start: int, end: int) -> Iterator[str]`
Генерирует номера карт в формате `XXXX XXXX XXXX XXXX`

**Тесты:**
- Корректность генерации в диапазоне 1-5
- Проверка формата вывода (4 группы по 4 цифры)
- Обработка граничных значений:
  - 0000 0000 0000 0001
  - 9999 9999 9999 9999
- Проверка валидации входных данных:
  - start > end (ValueError)
  - отрицательные значения (ValueError)

#### Примеры использования

```python
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Фильтрация транзакций
usd_transactions = filter_by_currency(transactions, "USD")
print(next(usd_transactions))

# Получение описаний
for desc in transaction_descriptions(transactions):
    print(desc)

# Генерация номеров карт
for card in card_number_generator(1, 5):
    print(card)
```

### Тестирование

Запуск всех тестов:
```bash
pytest -v tests/test_generators.py --cov=generators --cov-report=term-missing
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

### Module decorators

Декоратор `log` предоставляет гибкую систему логирования выполнения функций с возможностью вывода:
- В консоль (по умолчанию)
- В указанный файл (при задании параметра `filename`)

#### Декоратор логирования
`log(filename: Optional[str] = None) -> Callable`
Логирует выполнение функций с возможностью вывода в файл или консоль

**Тесты:**
- Логирование успешного выполнения:
  - В консоль (без filename)
  - В файл (с указанием filename)
  - Проверка формата сообщения (временная метка, имя функции)
  
- Логирование ошибок:
  - Запись типа исключения
  - Фиксация входных параметров
  - Проверка проброса исключения дальше
  
- Особые случаи:
  - Функции без аргументов
  - Функции с именованными аргументами
  - Функции возвращающие None
  - Функции с комплексными аргументами (словари, списки)
  
- Метаданные:
  - Сохранение __name__ оригинальной функции
  - Сохранение __doc__ оригинальной функции
  - Проверка типа возвращаемого значения (Callable)

#### Примеры использования

```python
from src.decorators import log

- "Логирование в консоль"
@log()
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)

- "Логирование в файл"
@log(filename="operations.log")
def divide(a: int, b: int) -> float:
    return a / b

divide(10, 2)
divide(5, 0)  # Запишет ошибку

- "Сложные аргументы"
@log()
def process(data: list[dict]) -> int:
    return len(data)

process([{"id": 1}, {"id": 2}])
```

### Тестирование

Запуск тестов:
```bash
pytest -v tests/test_decorators.py --cov=decorators --cov-report=term-missing
```

**Покрытие тестами:**
- Все основные сценарии использования
- Граничные случаи:
  - Пустые аргументы
  - Некорректные filename
  - Исключения разных типов
- Проверка метаданных функций
- 100% покрытие основного кода

**Дополнительные проверки:**
```bash
mypy decorators.py  # Проверка типов
flake8 decorators.py  # Проверка стиля
```

#### Структура логов

Успешное выполнение:
```
[YYYY-MM-DD HH:MM:SS] function_name ok
```

Ошибка выполнения:
```
[YYYY-MM-DD HH:MM:SS] function_name error: ErrorType. Inputs: (args,), {kwargs}
```

Файловый вывод:
- Создание файла при первом вызове
- Дописывание в существующий файл
- Кодировка UTF-8
```


## Запуск тестов

Для запуска всех тестов с проверкой покрытия:

```bash
pytest --cov=src --cov-report=html tests/
```

Отчет о покрытии будет сгенерирован в папке `htmlcov/`

## Требования к покрытию

Проект поддерживает:
- 100% покрытие для всех основных функций
- Тестирование всех граничных случаев
- Проверку обработки ошибок

## Дополнительные проверки

Запуск mypy для проверки типов:
```bash
mypy src/ tests/
```

Запуск flake8 для проверки стиля:
```bash
flake8 src/ tests/
```

## Документация

Полная документация по API доступна в исходных файлах:
- `src/masks.py` - маскировка номеров
- `src/widget.py` - основные функции интерфейса
- `src/processing.py` - обработка транзакций
- `src/generators.py` - генерация номеров карт
- `src/decorators.py` - логирование выполнения функций

## Лицензия

Этот проект распространяется под лицензией MIT.

```
Copyright (c) 2025 Rezilek

## Автор

Резиля Столярова 
Email: rezilek5177@gmail.com  
GitHub: [Rezilek](https://github.com/Rezilek)
