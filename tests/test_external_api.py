import os
from typing import Any, Dict
from unittest import TestCase, mock

import requests

from src.external_api import convert_transaction_amount


class TestConvertTransactionAmount(TestCase):
    def setUp(self) -> None:
        self.rub_transaction: Dict[str, Any] = {"amount": "100", "currency": "RUB"}
        self.usd_transaction: Dict[str, Any] = {"amount": "10", "currency": "USD"}
        self.eur_transaction: Dict[str, Any] = {"amount": "5", "currency": "EUR"}

    @mock.patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
    @mock.patch("requests.get")
    def test_convert_rub(self, mock_get: mock.Mock) -> None:
        result: float = convert_transaction_amount(self.rub_transaction)
        self.assertEqual(result, 100.0)
        mock_get.assert_not_called()

    @mock.patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
    @mock.patch("requests.get")
    def test_convert_usd(self, mock_get: mock.Mock) -> None:
        mock_response = mock.Mock()
        mock_response.json.return_value = {"rates": {"RUB": 75.5}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result: float = convert_transaction_amount(self.usd_transaction)
        self.assertEqual(result, 10 * 75.5)

    @mock.patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
    @mock.patch("requests.get")
    def test_convert_eur(self, mock_get: mock.Mock) -> None:
        mock_response = mock.Mock()
        mock_response.json.return_value = {"rates": {"RUB": 85.3}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result: float = convert_transaction_amount(self.eur_transaction)
        self.assertEqual(result, 5 * 85.3)

    @mock.patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
    def test_unsupported_currency(self) -> None:
        transaction: Dict[str, Any] = {"amount": "100", "currency": "GBP"}
        with self.assertRaises(ValueError):
            convert_transaction_amount(transaction)

    @mock.patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
    @mock.patch("requests.get")
    def test_api_error(self, mock_get: mock.Mock) -> None:
        mock_get.side_effect = requests.RequestException("API error")
        with self.assertRaises(ConnectionError):
            convert_transaction_amount(self.usd_transaction)
