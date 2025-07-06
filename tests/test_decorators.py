from pathlib import Path
from typing import Any, Callable, Generator

import pytest
from _pytest.capture import CaptureFixture
from _pytest.tmpdir import TempPathFactory

from src.decorators import log


def test_log_to_console_success(capsys: CaptureFixture[str]) -> None:
    """Тест успешного выполнения функции с выводом логов в консоль."""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result: int = add(1, 2)
    captured = capsys.readouterr()

    assert result == 3
    assert "add ok" in captured.out


def test_log_to_console_error(capsys: CaptureFixture[str]) -> None:
    """Тест ошибки в функции с выводом логов в консоль."""

    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0)" in captured.out


def test_log_to_file_success(tmp_path: Path) -> None:
    """Тест успешного выполнения функции с выводом логов в файл."""
    log_file: Path = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(a: int, b: int) -> int:
        return a * b

    result: int = multiply(3, 4)

    assert result == 12
    assert log_file.exists()

    content: str = log_file.read_text()
    assert "multiply ok" in content


def test_log_to_file_error(tmp_path: Path) -> None:
    """Тест ошибки в функции с выводом логов в файл."""
    log_file: Path = tmp_path / "test.log"

    @log(filename=str(log_file))
    def process_data(data: list) -> int:
        return len(data)

    with pytest.raises(TypeError):
        process_data(None)  # type: ignore

    assert log_file.exists()

    content: str = log_file.read_text()
    assert "process_data error: TypeError" in content
    assert "Inputs: (None,)" in content


def test_log_with_kwargs(capsys: CaptureFixture[str]) -> None:
    """Тест логирования функции с именованными аргументами."""

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result: str = greet("Alice", greeting="Hi")
    captured = capsys.readouterr()

    assert result == "Hi, Alice!"
    assert "greet ok" in captured.out


def test_log_with_complex_args(tmp_path: Path) -> None:
    """Тест логирования функции со сложными аргументами."""
    log_file: Path = tmp_path / "complex.log"

    @log(filename=str(log_file))
    def process_items(items: list[dict[str, Any]]) -> int:
        return sum(item.get("value", 0) for item in items)

    test_data: list[dict[str, Any]] = [{"value": 1}, {"value": 2}]
    result: int = process_items(test_data)

    assert result == 3

    content: str = log_file.read_text()
    assert "process_items ok" in content


@pytest.fixture
def log_fixture(tmp_path_factory: TempPathFactory) -> Generator[Path, None, None]:
    """Фикстура для временного лог-файла."""
    log_dir: Path = tmp_path_factory.mktemp("logs")
    log_file: Path = log_dir / "fixture_test.log"
    yield log_file
    if log_file.exists():
        log_file.unlink()


def test_log_with_fixture(log_fixture: Path) -> None:
    """Тест логирования с использованием фикстуры."""

    @log(filename=str(log_fixture))
    def power(base: int, exponent: int) -> int:
        return base**exponent

    result: int = power(2, 3)

    assert result == 8
    assert log_fixture.exists()

    content: str = log_fixture.read_text()
    assert "power ok" in content


def test_log_function_metadata() -> None:
    """Тест сохранения метаданных оригинальной функции."""

    @log()
    def original_func(x: int) -> int:
        """Оригинальная функция."""
        return x * 2

    assert original_func.__name__ == "original_func"
    assert original_func.__doc__ == "Оригинальная функция."
    assert isinstance(original_func, Callable)
