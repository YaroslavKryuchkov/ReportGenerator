import sys
from unittest.mock import patch
import pytest
from report_generator import load_data, main
from reporter import Reporter


def test_load_data_multiple_files(temp_csv_file, sample_csv_data):
    """Проверка загрузки данных из двух одинаковых файлов (записи объединяются)."""
    data = load_data([temp_csv_file, temp_csv_file])
    assert "Алексей Смирнов" in data
    assert len(data["Алексей Смирнов"]) == 4
    assert data["Алексей Смирнов"][0]["coffee_spent"] == "450"
    assert data["Алексей Смирнов"][1]["coffee_spent"] == "500"
    assert data["Дарья Петрова"][2]["coffee_spent"] == "200"


def test_load_data_multiple_files_with_same_student(tmp_path):
    """Данные одного студента из разных файлов объединяются в один список."""
    file1 = tmp_path / "file1.csv"
    file1.write_text(
        "student,coffee_spent\nПетров,100\n",
        encoding="utf-8"
    )
    file2 = tmp_path / "file2.csv"
    file2.write_text(
        "student,coffee_spent\nПетров,200\n",
        encoding="utf-8"
    )
    data = load_data([str(file1), str(file2)])
    assert "Петров" in data
    assert len(data["Петров"]) == 2
    assert data["Петров"][0]["coffee_spent"] == "100"
    assert data["Петров"][1]["coffee_spent"] == "200"


def test_median_coffee_report_even_count():
    """Проверка медианы при чётном количестве значений (на данных в новом формате)."""
    data = {
        "Student": [
            {"coffee_spent": "10"},
            {"coffee_spent": "20"},
            {"coffee_spent": "30"},
            {"coffee_spent": "40"}
        ]
    }
    reporter = Reporter()
    rows, headers = reporter.run("median-coffee", data)
    assert rows[0][1] == 25.0


def test_median_coffee_report_same_median():
    """При одинаковой медиане порядок стабилен (сортировка по убыванию)."""
    data = {
        "A": [{"coffee_spent": "10"}, {"coffee_spent": "20"}],
        "B": [{"coffee_spent": "15"}, {"coffee_spent": "15"}]
    }
    reporter = Reporter()
    rows, _ = reporter.run("median-coffee", data)
    medians = [row[1] for row in rows]
    assert medians == [15.0, 15.0]


@patch('sys.argv', ['report_generator.py', '--files', 'a.csv', 'b.csv', '--report', 'median-coffee'])
@patch('report_generator.load_data')
@patch('report_generator.tabulate')
def test_main_multiple_files(mock_tabulate, mock_load_data):
    """Проверка, что main передаёт все файлы в load_data."""
    mock_load_data.return_value = {"Student A": [{"coffee_spent": "100"}, {"coffee_spent": "200"}]}
    with patch('sys.stdout'):
        main()
    mock_load_data.assert_called_once_with(['a.csv', 'b.csv'])


@patch('sys.argv', ['report_generator.py', '--files', 'test.csv', '--report', 'median-coffee'])
@patch('report_generator.load_data')
@patch('report_generator.tabulate')
def test_main_empty_data(mock_tabulate, mock_load_data):
    """При отсутствии данных программа завершается с ошибкой."""
    mock_load_data.return_value = {}
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    mock_tabulate.assert_not_called()


@patch('sys.argv', ['report_generator.py', '--files', 'test.csv', '--report', 'median-coffee'])
@patch('report_generator.load_data')
@patch('report_generator.tabulate')
def test_main_error_in_report(mock_tabulate, mock_load_data):
    """Если отчёт выбрасывает исключение, оно перехватывается и программа завершается."""
    mock_load_data.return_value = {"Student A": [{"coffee_spent": "1"}]}
    with patch('reporter.Reporter.run', side_effect=Exception("Test error")):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    mock_tabulate.assert_not_called()