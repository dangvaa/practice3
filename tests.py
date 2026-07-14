import pytest
from engine import AnalyzerEngine


@pytest.fixture
def engine():
    """Создает экземпляр анализатора с тестовыми правилами."""
    mock_rules = [
        {"id": "STU-PY-01", "severity": "MAJOR", "description": "Resource Leak"},
        {"id": "STU-PY-02", "severity": "MAJOR", "description": "Silent Exception"},
        {"id": "STU-PY-03", "severity": "MAJOR", "description": "Complexity"},
        {"id": "STU-PY-04", "severity": "MINOR", "description": "Naming"},
        {"id": "STU-PY-05", "severity": "MINOR", "description": "Docstring"},
        {"id": "STU-PY-06", "severity": "MAJOR", "description": "Paths"},
    ]
    return AnalyzerEngine(mock_rules)


def test_missing_with_negative(engine):
    """Проверяет, что вызов open() без with вызывает ошибку STU-PY-01."""
    code = "f = open('data.txt', 'r')"
    issues, _ = engine.run(code)
    assert any(i.rule_id == "STU-PY-01" for i in issues)


def test_silent_except_negative(engine):
    """Проверяет, что пустой except вызывает ошибку STU-PY-02."""
    code = "try:\n    1/0\nexcept:\n    pass"
    issues, _ = engine.run(code)
    assert any(i.rule_id == "STU-PY-02" for i in issues)


def test_high_complexity_negative(engine):
    """Проверяет, что сложная функция вызывает ошибку STU-PY-03."""
    code = "def complex_func():\n"
    for i in range(11):
        code += f"    if {i} > 0: print({i})\n"
    issues, _ = engine.run(code)
    assert any(i.rule_id == "STU-PY-03" for i in issues)


def test_naming_convention_negative(engine):
    """Проверяет, что нарушение именования вызывает ошибку STU-PY-04."""
    code = "def badName(): pass"
    issues, _ = engine.run(code)
    assert any(i.rule_id == "STU-PY-04" for i in issues)


def test_missing_docstring_negative(engine):
    """Проверяет, что отсутствие docstring вызывает ошибку STU-PY-05."""
    code = "def no_doc():\n    pass"
    issues, _ = engine.run(code)
    assert any(i.rule_id == "STU-PY-05" for i in issues)


def test_absolute_paths_negative(engine):
    """Проверяет, что абсолютный путь вызывает ошибку STU-PY-06."""
    code = 'path = r"C:/Users/Admin/data.csv"'
    issues, _ = engine.run(code)
    assert any(i.rule_id == "STU-PY-06" for i in issues)


def test_clean_code_positive(engine):
    """Проверяет, что корректный код не вызывает ни одной ошибки."""
    clean_code = """
def good_function_name(x):
    \"\"\"Правильная документация.\"\"\"
    with open('file.txt', 'r') as f:
        data = f.read()
    
    try:
        return x / len(data)
    except ZeroDivisionError:
        print("Ошибка деления")
        return 0

path = "data/relative/path.txt"
    """
    issues, _ = engine.run(clean_code)

    assert len(issues) == 0


def test_naming_and_docstring_positive(engine):
    """Проверяет, что корректное именование и docstring не вызывают ошибок."""
    code = 'def correct_name():\n    """Doc."""\n    pass'
    issues, _ = engine.run(code)
    assert not any(i.rule_id in ["STU-PY-04", "STU-PY-05"] for i in issues)


def test_relative_path_positive(engine):
    """Проверяет, что относительный путь не вызывает ошибку STU-PY-06."""
    code = 'path = "assets/images/logo.png"'
    issues, _ = engine.run(code)
    assert not any(i.rule_id == "STU-PY-06" for i in issues)