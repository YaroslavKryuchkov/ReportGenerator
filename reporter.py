import statistics
from typing import Dict, List, Any, Tuple


class Reporter:

    def median_coffee(self, data: Dict[str, List[Dict[str, Any]]]) -> Tuple[List[Tuple[str, float]], List[str]]:
        """
        Отчёт: медианная сумма трат на кофе по каждому студенту.
        Возвращает строки таблицы и заголовки.
        """
        rows = []
        for student, records in data.items():
            spends = []
            for rec in records:
                try:
                    spends.append(int(rec.get("coffee_spent", 0)))
                except (KeyError, ValueError):
                    continue
            if spends:
                median_spent = statistics.median(spends)
                rows.append((student, median_spent))
        rows.sort(key=lambda x: x[1], reverse=True)
        headers = ["Студент", "Медиана трат на кофе"]
        return rows, headers

    def run(self, report_name: str, data: Dict[str, List[Dict[str, Any]]]) -> Tuple[List, List[str]]:
        method_name = report_name.replace('-', '_')
        method = getattr(self, method_name, None)
        if method is None:
            raise ValueError(f"Неизвестный отчёт: {report_name}")
        return method(data)