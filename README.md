<h1 align="center">Генератор отчётов</h1>
Генерирует отчёты из .csv файлов и выводит таблицу отчёта в консоль.

<h2 align="center">Требования</h2>
Основные:
python 3.10+
tabulate

Для тестов:
pytest
pytest-cov

Для легкой установки зависимостей успользуйте данную команду:
pip install -r requirements.txt

<h2 align="center">Пример ввызова</h2>
python report_generator.py --files path/to/data.csv can/be/multiple/data/sources.csv --report report_method_name

<h2 align="center">Доступные отчёты</h2>
median-coffee - медианная сумма трат на кофе по каждому студенту

<h3>Тестовые файлы</h3>
В папке testfiles есть тестовые .csv файлы и значения при вызове<br>
python report_generator.py --files path/to/data.csv can/be/multiple/data/sources.csv --report median-coffee

<h2 align="center">Добавление нового отчёта</h2>
1.Создайте метод в reporter.py.<br>
2.Метод должен возвращать (rows, headers) для tabulate.<br>
3.Вызывайте через --report <method_name><br>

Пример:<br>
def average_coffee(self, data: Dict[str, List[Dict[str, Any]]]) -> Tuple[List[Tuple[str, float]], List[str]]:<br>
    # ваша логика<br>
    return rows, headers
    
