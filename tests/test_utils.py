import json
import os
import tempfile
from typing import Any, Dict, List
from unittest import TestCase

from src.utils import read_json_file


class TestReadJsonFile(TestCase):
    def setUp(self) -> None:
        self.valid_data: List[Dict[str, Any]] = [
            {"id": 1, "amount": 100, "currency": "RUB"},
            {"id": 2, "amount": 200, "currency": "USD"},
        ]

    def test_read_valid_json(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(self.valid_data, f)
            file_path: str = f.name

        try:
            result: List[Dict[str, Any]] = read_json_file(file_path)
            self.assertEqual(result, self.valid_data)
        finally:
            os.unlink(file_path)

    def test_read_empty_file(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            file_path: str = f.name

        try:
            result: List[Dict[str, Any]] = read_json_file(file_path)
            self.assertEqual(result, [])
        finally:
            os.unlink(file_path)

    def test_read_non_list_json(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"key": "value"}, f)
            file_path: str = f.name

        try:
            result: List[Dict[str, Any]] = read_json_file(file_path)
            self.assertEqual(result, [])
        finally:
            os.unlink(file_path)

    def test_read_nonexistent_file(self) -> None:
        result: List[Dict[str, Any]] = read_json_file("nonexistent_file.json")
        self.assertEqual(result, [])
