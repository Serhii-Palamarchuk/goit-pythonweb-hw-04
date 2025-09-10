#!/usr/bin/env python3
"""
Скрипт для створення тестових файлів для перевірки async_file_sorter.py
"""

from pathlib import Path


def create_test_files():
    """Створює тестові файли для демонстрації роботи сортувальника."""

    # Створюємо папку для тестових файлів
    test_folder = Path("test_files")
    test_folder.mkdir(exist_ok=True)

    # Створюємо підпапки
    (test_folder / "documents").mkdir(exist_ok=True)
    (test_folder / "images").mkdir(exist_ok=True)
    (test_folder / "mixed").mkdir(exist_ok=True)

    # Список тестових файлів
    test_files = [
        # Текстові файли
        ("document1.txt", "Це тестовий текстовий документ 1"),
        ("document2.txt", "Це тестовий текстовий документ 2"),
        ("readme.md", "# Readme файл\nЦе markdown документ"),
        # Файли документів
        ("documents/report.docx", "Тестовий Word документ"),
        ("documents/presentation.pptx", "Тестова презентація"),
        ("documents/spreadsheet.xlsx", "Тестова таблиця"),
        ("documents/document.pdf", "Тестовий PDF документ"),
        # Файли зображень (створюємо фіктивні)
        ("images/photo1.jpg", "Фіктивний JPEG файл"),
        ("images/photo2.png", "Фіктивний PNG файл"),
        ("images/logo.gif", "Фіктивний GIF файл"),
        ("images/vector.svg", "<svg>Фіктивний SVG файл</svg>"),
        # Змішані файли
        ("mixed/script.py", "print('Hello, World!')"),
        ("mixed/style.css", "body { margin: 0; }"),
        ("mixed/page.html", "<html><body>Test</body></html>"),
        ("mixed/data.json", '{"test": "data"}'),
        ("mixed/config.xml", "<config><setting>value</setting></config>"),
        # Файл без розширення
        ("no_ext_file", "Файл без розширення"),
        # Файли з великими літерами в розширенні
        ("UPPERCASE.TXT", "Файл з великими літерами в розширенні"),
        ("MixedCase.PDF", "Файл зі змішаним регістром"),
    ]

    # Створюємо всі тестові файли
    for file_path, content in test_files:
        full_path = test_folder / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Створено: {full_path}")

    print(
        f"\nВсього створено {len(test_files)} тестових файлів "
        f"у папці '{test_folder}'"
    )
    print("Тепер ви можете запустити сортувальник:")
    print(f"python async_file_sorter.py {test_folder} sorted_files")


if __name__ == "__main__":
    create_test_files()
