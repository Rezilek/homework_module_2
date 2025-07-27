from typing import Any, Dict

from src.file_reader import read_csv, read_excel
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import read_json_file
from src.widget import get_date, mask_account_card


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода."""
    date = get_date(transaction["date"])
    description = transaction["description"]

    # Маскировка реквизитов
    from_ = mask_account_card(transaction["from"]) if "from" in transaction else None
    to_ = mask_account_card(transaction["to"])

    # Формирование строки перевода
    transfer_line = f"{from_} -> {to_}" if from_ else str(to_)

    # Информация о сумме
    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["name"]

    return f"{date} {description}\n{transfer_line}\nСумма: {amount} {currency}"


def main() -> None:
    """Основная логика программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор источника данных
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()
    file_paths = {
        "1": ("data/operations.json", "JSON"),
        "2": ("data/transactions.csv", "CSV"),
        "3": ("data/transactions.xlsx", "XLSX"),
    }

    if choice not in file_paths:
        print("Неверный выбор. Завершение программы.")
        return

    file_path, file_type = file_paths[choice]
    print(f"\nДля обработки выбран {file_type}-файл.")

    # Чтение данных
    try:
        if choice == "1":
            data = read_json_file(file_path)
        elif choice == "2":
            data = read_csv(file_path)
        else:
            data = read_excel(file_path)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input("\nВведите статус операции (EXECUTED/CANCELED/PENDING): ").strip().upper()
        if status in valid_statuses:
            break
        print(f'Статус операции "{status}" недоступен. Попробуйте снова.')

    filtered_data = filter_by_state(data, status)
    print(f"\nОперации отфильтрованы по статусу '{status}'")

    # Дополнительные фильтры
    if input("\nОтсортировать операции по дате? (Да/Нет): ").lower() == "да":
        order = input("По возрастанию или по убыванию? (возрастание/убывание): ").lower()
        reverse = order == "убывание"
        filtered_data = sort_by_date(filtered_data, reverse)

    if input("\nВыводить только рублевые транзакции? (Да/Нет): ").lower() == "да":
        filtered_data = [t for t in filtered_data if t["operationAmount"]["currency"]["code"] == "RUB"]

    if input("\nФильтровать по ключевому слову в описании? (Да/Нет): ").lower() == "да":
        keyword = input("Введите слово для поиска: ").strip()
        filtered_data = process_bank_search(filtered_data, keyword)

    # Вывод результатов
    if not filtered_data:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия")
    else:
        print(f"\nВсего банковских операций в выборке: {len(filtered_data)}")
        for transaction in filtered_data:
            print("\n" + format_transaction(transaction))


if __name__ == "__main__":
    main()
