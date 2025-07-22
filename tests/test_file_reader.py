import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from src.file_reader import read_csv, read_excel


class TestFileReader(unittest.TestCase):
    def test_read_csv(self):
        """Тест чтения CSV файла."""
        csv_content = (
            "id,date,amount,currency\n"
            "1,2023-01-01,100,USD\n"
            "2,2023-01-02,200,EUR\n"
        )
        expected = [
            {"id": "1", "date": "2023-01-01", "amount": "100", "currency": "USD"},
            {"id": "2", "date": "2023-01-02", "amount": "200", "currency": "EUR"},
        ]

        with patch("builtins.open", mock_open(read_data=csv_content)):
            result = read_csv("dummy_path.csv")
            self.assertEqual(result, expected)

    @patch("pandas.read_excel")
    def test_read_excel(self, mock_read_excel):
        """Тест чтения Excel файла."""
        mock_data = pd.DataFrame({
            "id": [1, 2],
            "date": ["2023-01-01", "2023-01-02"],
            "amount": [100, 200],
            "currency": ["USD", "EUR"]
        })
        mock_read_excel.return_value = mock_data

        expected = [
            {"id": 1, "date": "2023-01-01", "amount": 100, "currency": "USD"},
            {"id": 2, "date": "2023-01-02", "amount": 200, "currency": "EUR"},
        ]

        result = read_excel("dummy_path.xlsx")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()