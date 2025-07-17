import logging
import os
from pathlib import Path


def setup_logger(name: str, log_file: str) -> logging.Logger:
    """Настройка логера с указанным именем и файлом."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Обработчик для записи в файл (с перезаписью при каждом запуске)
    file_handler = logging.FileHandler(logs_dir / log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Форматтер с меткой времени, именем модуля, уровнем и сообщением
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
