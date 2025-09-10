"""Тести для асинхронного сортувальника файлів."""

import os
import sys
import tempfile
from pathlib import Path
import pytest

# Додаємо кореневу папку проекту до sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from async_file_sorter import (  # noqa: E402
    read_folder,
    copy_file,
    process_files,
)


@pytest.mark.asyncio
async def test_read_folder_empty():
    """Тест читання порожньої папки."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        files = await read_folder(temp_path)
        assert files == []


@pytest.mark.asyncio
async def test_read_folder_with_files():
    """Тест читання папки з файлами."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Створюємо тестові файли
        test_file1 = temp_path / "test1.txt"
        test_file2 = temp_path / "test2.py"
        test_file1.write_text("test content 1")
        test_file2.write_text("test content 2")

        files = await read_folder(temp_path)

        assert len(files) == 2
        assert test_file1 in files
        assert test_file2 in files


@pytest.mark.asyncio
async def test_copy_file():
    """Тест копіювання файлу."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Створюємо тестовий файл
        source_file = temp_path / "source.txt"
        source_file.write_text("test content")

        # Створюємо папку призначення
        output_dir = temp_path / "output"

        # Копіюємо файл
        await copy_file(source_file, output_dir)

        # Перевіряємо результат
        expected_file = output_dir / "txt" / "source.txt"
        assert expected_file.exists()
        assert expected_file.read_text() == "test content"


@pytest.mark.asyncio
async def test_copy_file_no_extension():
    """Тест копіювання файлу без розширення."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Створюємо тестовий файл без розширення
        source_file = temp_path / "noext"
        source_file.write_text("test content")

        # Створюємо папку призначення
        output_dir = temp_path / "output"

        # Копіюємо файл
        await copy_file(source_file, output_dir)

        # Перевіряємо результат
        expected_file = output_dir / "no_extension" / "noext"
        assert expected_file.exists()
        assert expected_file.read_text() == "test content"


@pytest.mark.asyncio
async def test_process_files_integration():
    """Інтеграційний тест повного процесу сортування."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Створюємо вихідну папку з файлами
        source_dir = temp_path / "source"
        source_dir.mkdir()

        test_files = [
            ("doc1.txt", "text content"),
            ("image.jpg", "fake jpg content"),
            ("script.py", "print('hello')"),
            ("noext", "no extension file"),
        ]

        for filename, content in test_files:
            (source_dir / filename).write_text(content)

        # Створюємо папку призначення
        output_dir = temp_path / "output"

        # Виконуємо сортування
        await process_files(source_dir, output_dir)

        # Перевіряємо результати
        assert (output_dir / "txt" / "doc1.txt").exists()
        assert (output_dir / "jpg" / "image.jpg").exists()
        assert (output_dir / "py" / "script.py").exists()
        assert (output_dir / "no_extension" / "noext").exists()

        # Перевіряємо вміст файлів
        assert (output_dir / "txt" / "doc1.txt").read_text() == "text content"
        script_content = (output_dir / "py" / "script.py").read_text()
        assert script_content == "print('hello')"


def test_argument_parser():
    """Тест парсера аргументів."""
    from async_file_sorter import create_argument_parser

    parser = create_argument_parser()

    # Тест з валідними аргументами
    args = parser.parse_args(["source_folder", "output_folder"])
    assert args.source == "source_folder"
    assert args.output == "output_folder"
    assert args.verbose is False

    # Тест з verbose прапором
    args = parser.parse_args(["source", "output", "--verbose"])
    assert args.verbose is True
