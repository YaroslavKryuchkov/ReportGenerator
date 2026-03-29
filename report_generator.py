import argparse
import csv
import sys
from typing import Dict, List, Any

from tabulate import tabulate

from reporter import Reporter


def load_data(files: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    data: Dict[str, List[Dict[str, Any]]] = {}
    for filename in files:
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    student = row.get("student", "").strip()
                    if student:
                        data.setdefault(student, []).append(row)
        except FileNotFoundError:
            print(f"Файл не найден: {filename}", file=sys.stderr)
        except Exception as e:
            print(f"Ошибка при чтении файла {filename}: {e}", file=sys.stderr)
    return data


def main():
    parser = argparse.ArgumentParser(description="Обработка CSV-файлов студентов")
    parser.add_argument("--files", nargs="+", required=True, help="Список CSV-файлов для обработки")
    parser.add_argument("--report", required=True, help="Название отчёта (например, 'median-coffee')")
    args = parser.parse_args()

    data = load_data(args.files)
    if not data:
        print("Нет данных для формирования отчёта.", file=sys.stderr)
        sys.exit(1)

    reporter = Reporter()
    try:
        table_data, headers = reporter.run(args.report, data)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при формировании отчёта: {e}", file=sys.stderr)
        sys.exit(1)

    print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()