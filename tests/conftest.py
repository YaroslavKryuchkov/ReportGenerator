import pytest
import tempfile


@pytest.fixture
def sample_csv_data():
    """Возвращает содержимое валидного CSV-файла."""
    return """student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика
Алексей Смирнов,2024-06-02,500,4.0,14,устал,Математика
Дарья Петрова,2024-06-01,200,7.0,6,отл,Математика
Дарья Петрова,2024-06-02,250,6.5,8,норм,Математика
"""


@pytest.fixture
def temp_csv_file(sample_csv_data):
    """Создаёт временный CSV-файл с данными."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', encoding='utf-8', delete=False) as f:
        f.write(sample_csv_data)
        return f.name