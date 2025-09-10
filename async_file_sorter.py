#!/usr/bin/env python3
"""
Асинхронний скрипт для сортування файлів за розширеннями.
Читає всі файли у вихідній папці та розподіляє їх по підпапках
у цільовій директорії на основі розширення файлів.
"""

import asyncio
import argparse
import logging
from pathlib import Path
import aiofiles
import aiofiles.os
from typing import List


# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("file_sorter.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def read_folder(source_folder: Path) -> List[Path]:
    """
    Асинхронно рекурсивно читає всі файли у вихідній папці та її підпапках.

    Args:
        source_folder (Path): Шлях до вихідної папки

    Returns:
        List[Path]: Список всіх файлів у папці та підпапках
    """
    files = []

    try:
        # Перевіряємо, чи існує папка
        if not source_folder.exists():
            logger.error(f"Вихідна папка не існує: {source_folder}")
            return files

        if not source_folder.is_dir():
            logger.error(f"Вказаний шлях не є папкою: {source_folder}")
            return files

        logger.info(f"Читання папки: {source_folder}")

        # Рекурсивно обходимо всі файли та папки
        for item in source_folder.rglob("*"):
            if item.is_file():
                files.append(item)
                logger.debug(f"Знайдено файл: {item}")

        logger.info(f"Знайдено {len(files)} файлів у папці {source_folder}")

    except PermissionError as e:
        logger.error(f"Немає доступу до папки {source_folder}: {e}")
    except Exception as e:
        logger.error(f"Помилка при читанні папки {source_folder}: {e}")

    return files


async def copy_file(file_path: Path, output_folder: Path) -> None:
    """
    Асинхронно копіює файл у відповідну підпапку на основі його розширення.

    Args:
        file_path (Path): Шлях до файлу для копіювання
        output_folder (Path): Цільова папка для копіювання
    """
    try:
        # Отримуємо розширення файлу (без крапки)
        extension = file_path.suffix.lower().lstrip(".")

        # Якщо немає розширення, використовуємо папку "no_extension"
        if not extension:
            extension = "no_extension"

        # Створюємо підпапку для розширення
        target_dir = output_folder / extension

        # Асинхронно створюємо директорію, якщо вона не існує
        try:
            await aiofiles.os.makedirs(target_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"Не вдалося створити директорію {target_dir}: {e}")
            return

        # Формуємо шлях до цільового файлу
        target_file = target_dir / file_path.name

        # Якщо файл з таким іменем вже існує, додаємо номер
        counter = 1
        original_target = target_file
        while target_file.exists():
            stem = original_target.stem
            suffix = original_target.suffix
            target_file = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        # Асинхронно копіюємо файл
        async with aiofiles.open(file_path, "rb") as src:
            async with aiofiles.open(target_file, "wb") as dst:
                content = await src.read()
                await dst.write(content)

        logger.info(f"Скопійовано: {file_path} -> {target_file}")

    except PermissionError as e:
        logger.error(f"Немає доступу до файлу {file_path}: {e}")
    except FileNotFoundError as e:
        logger.error(f"Файл не знайдено {file_path}: {e}")
    except Exception as e:
        logger.error(f"Помилка при копіюванні файлу {file_path}: {e}")


async def process_files(source_folder: Path, output_folder: Path) -> None:
    """
    Основна функція для обробки файлів.

    Args:
        source_folder (Path): Вихідна папка
        output_folder (Path): Цільова папка
    """
    try:
        # Створюємо цільову папку, якщо вона не існує
        await aiofiles.os.makedirs(output_folder, exist_ok=True)
        logger.info(f"Цільова папка готова: {output_folder}")

        # Читаємо всі файли з вихідної папки
        files = await read_folder(source_folder)

        if not files:
            logger.warning("Не знайдено файлів для обробки")
            return

        # Створюємо задачі для асинхронного копіювання всіх файлів
        tasks = [copy_file(file_path, output_folder) for file_path in files]

        # Виконуємо всі задачі асинхронно
        logger.info(f"Початок копіювання {len(tasks)} файлів...")
        await asyncio.gather(*tasks)

        logger.info("Сортування файлів завершено успішно!")

    except Exception as e:
        logger.error(f"Критична помилка в process_files: {e}")


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Створює та налаштовує ArgumentParser для обробки аргументів
    командного рядка.

    Returns:
        argparse.ArgumentParser: Налаштований парсер аргументів
    """
    parser = argparse.ArgumentParser(
        description="Асинхронне сортування файлів за розширеннями",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:
  python async_file_sorter.py source_folder output_folder
  python async_file_sorter.py C:\\Documents C:\\SortedFiles
  python async_file_sorter.py /home/user/docs /home/user/sorted
        """,
    )

    parser.add_argument(
        "source",
        type=str,
        help="Шлях до вихідної папки з файлами для сортування",
    )

    parser.add_argument(
        "output",
        type=str,
        help="Шлях до цільової папки для розподілених файлів",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Детальний вивід (debug режим)",
    )

    return parser


async def main():
    """Головна функція програми."""
    # Створюємо та налаштовуємо парсер аргументів
    parser = create_argument_parser()
    args = parser.parse_args()

    # Налаштовуємо рівень логування
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Ініціалізуємо асинхронні шляхи
    source_folder = Path(args.source).resolve()
    output_folder = Path(args.output).resolve()

    logger.info(f"Вихідна папка: {source_folder}")
    logger.info(f"Цільова папка: {output_folder}")

    # Перевіряємо, чи вихідна та цільова папки не збігаються
    if source_folder == output_folder:
        logger.error("Вихідна та цільова папки не можуть бути однаковими!")
        return

    # Перевіряємо, чи цільова папка не знаходиться всередині вихідної
    try:
        output_folder.relative_to(source_folder)
        logger.error("Цільова папка не може знаходитися всередині вихідної папки!")
        return
    except ValueError:
        # Це нормально - папки не пов'язані
        pass

    # Запускаємо асинхронну обробку файлів
    await process_files(source_folder, output_folder)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Програма перервана користувачем")
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
