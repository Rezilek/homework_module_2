import json
import os
from typing import Any, Dict, List
from src.log_config import setup_logger

# Настройка логера для модуля utils
logger = setup_logger('utils_module', 'utils.log')


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Читает JSON-файл с транзакциями."""
    try:
        logger.debug(f"Начало чтения файла: {file_path}")

        if not os.path.exists(file_path):
            error_msg = f"Файл не найден: {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            error_msg = f"Файл {file_path} не содержит список"
            logger.warning(error_msg)
            return []

        logger.info(f"Успешно прочитано {len(data)} транзакций из {file_path}")
        return data

    except json.JSONDecodeError as e:
        error_msg = f"Ошибка декодирования JSON в {file_path}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return []
    except Exception as e:
        error_msg = f"Неожиданная ошибка при чтении {file_path}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return []


if __name__ == '__main__':
    # Демонстрация работы с логированием
    import tempfile
    import os

    print("\nДемонстрация работы utils.py:")

    # Создание тестового JSON файла
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.json', delete=False) as tmp:
        tmp.write('[{"id": 1}, {"id": 2}]')
        test_file = tmp.name

    # Успешное чтение
    print("Успешное чтение:", read_json_file(test_file))

    # Чтение несуществующего файла
    print("Чтение отсутствующего файла:", read_json_file("non_existent.json"))

    # Создание файла с невалидным JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp.write('{invalid json}')
        invalid_json = tmp.name

    # Чтение битого JSON
    print("Чтение битого JSON:", read_json_file(invalid_json))

    # Создание файла с не-списком
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp.write('{"key": "value"}')
        not_list = tmp.name

    # Чтение JSON не являющегося списком
    print("Чтение JSON-объекта:", read_json_file(not_list))

    # Удаление временных файлов
    os.unlink(test_file)
    os.unlink(invalid_json)
    os.unlink(not_list)

    print("Проверьте логи в logs/utils.log")
