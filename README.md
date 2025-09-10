# GoIT Python Web HW-04: Асинхронне сортування файлів

Цей проект містить Python-скрипт для асинхронного сортування файлів за їх розширеннями.

## Опис

Скрипт читає всі файли у вказаній користувачем вихідній папці (source folder) і розподіляє їх по підпапках у директорії призначення (output folder) на основі розширення файлів. Сортування виконується асинхронно для більш ефективної обробки великої кількості файлів.

## Встановлення

1. Клонуйте репозиторій:
```bash
git clone https://github.com/Serhii-Palamarchuk/goit-pythonweb-hw-04.git
cd goit-pythonweb-hw-04
```

2. Встановіть Poetry (якщо ще не встановлений):
```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -
```

3. Встановіть залежності проекту:
```bash
poetry install
```

## Використання

```bash
# Базове використання
poetry run python async_file_sorter.py <source_folder> <output_folder>

# Або через встановлену команду
poetry run async-file-sorter <source_folder> <output_folder>
```

### Приклади:

```bash
# Базове використання
poetry run python async_file_sorter.py ./source_files ./sorted_files

# З детальним виводом
poetry run python async_file_sorter.py ./source_files ./sorted_files --verbose

# Windows шляхи
poetry run python async_file_sorter.py "C:\Documents" "C:\SortedFiles"

# Unix шляхи  
poetry run python async_file_sorter.py /home/user/docs /home/user/sorted

# Створення тестових файлів для демонстрації
poetry run python create_test_files.py
```

## Функціональність

- **Асинхронне копіювання**: Всі файли копіюються паралельно для максимальної продуктивності
- **Рекурсивне читання**: Обробляються всі файли у підпапках
- **Автоматичне створення папок**: Створюються папки для кожного розширення файлів
- **Обробка конфліктів імен**: Автоматичне додавання номерів до файлів з однаковими іменами
- **Логування**: Детальне логування всіх операцій та помилок
- **Валідація**: Перевірка шляхів та запобігання некоректним операціям

## Структура вихідних папок

Файли розподіляються по папках за розширенням:
```
output_folder/
├── txt/
│   ├── document1.txt
│   └── document2.txt
├── pdf/
│   └── presentation.pdf
├── jpg/
│   ├── photo1.jpg
│   └── photo2.jpg
├── no_extension/
│   └── readme
└── ...
```

## Логування

Скрипт створює файл логу `file_sorter.log` та виводить інформацію в консоль. Використовуйте прапор `--verbose` для детального виводу.

## Технічні деталі

- Використовує `asyncio` для асинхронної обробки
- `aiofiles` для асинхронного читання/запису файлів
- `pathlib` для роботи зі шляхами
- `argparse` для обробки аргументів командного рядка
- Повна відповідність стандартам PEP 8

## Вимоги

- Python 3.8.1+
- Poetry для управління залежностями

## Залежності

- `aiofiles` - для асинхронної роботи з файлами

## Розробка

Для розробників доступні додаткові інструменти:

```bash
# Форматування коду
poetry run black .

# Перевірка стилю коду
poetry run flake8 .

# Статична перевірка типів
poetry run mypy async_file_sorter.py

# Запуск тестів (коли будуть додані)
poetry run pytest
```

## Автор

Serhii Palamarchuk
Тема 4. Асинхронне програмування в Python
