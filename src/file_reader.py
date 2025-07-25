import csv
from typing import Dict, List, Union

import pandas as pd


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу.

    Returns:
        Список словарей с транзакциями.
    """
    transactions = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(dict(row))
    return transactions


def read_excel(file_path: str, sheet_name: Union[str, int] = 0) -> List[Dict]:
    """Считывает финансовые операции из Excel-файла.

    Args:
        file_path: Путь к Excel-файлу.
        sheet_name: Название или индекс листа (по умолчанию 0).

    Returns:
        Список словарей с транзакциями.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df.replace({float("nan"): None}).to_dict(orient="records")
