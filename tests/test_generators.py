# Тесты для модуля generators

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет75106830613657916952",
            "to": "Счет11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет19708645243227258542",
            "to": "Счет75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет44812258784861134719",
            "to": "Счет74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic6831982476737658",
            "to": "Visa Platinum8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum1246377376343588",
            "to": "Счет14211924144426031657",
        },
    ]


class TestFilterByCurrency:
    def test_filter_usd_transactions(self, sample_transactions):
        usd_transactions = filter_by_currency(sample_transactions, "USD")
        result = list(usd_transactions)
        assert len(result) == 3
        assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)

    def test_filter_rub_transactions(self, sample_transactions):
        rub_transactions = filter_by_currency(sample_transactions, "RUB")
        result = list(rub_transactions)
        assert len(result) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in result)

    def test_filter_empty_list(self):
        result = list(filter_by_currency([], "USD"))
        assert len(result) == 0

    def test_filter_no_matching_currency(self, sample_transactions):
        result = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(result) == 0


class TestTransactionDescriptions:
    def test_descriptions_generator(self, sample_transactions):
        descriptions = transaction_descriptions(sample_transactions)
        result = list(descriptions)
        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
        assert result == expected

    def test_empty_transactions(self):
        descriptions = transaction_descriptions([])
        assert list(descriptions) == []


class TestCardNumberGenerator:
    @pytest.mark.parametrize(
        "start, end, expected",
        [
            (1, 1, ["0000 0000 0000 0001"]),
            (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
            (9999, 10001, ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001"]),
        ],
    )
    def test_generator_output(self, start, end, expected):
        assert list(card_number_generator(start, end)) == expected

    def test_large_range(self):
        generator = card_number_generator(1, 100)
        result = list(generator)
        assert len(result) == 100
        assert result[0] == "0000 0000 0000 0001"
        assert result[-1] == "0000 0000 0000 0100"

    def test_format_correctness(self):
        number = next(card_number_generator(1234567890123456, 1234567890123456))
        assert number == "1234 5678 9012 3456"
