# Руководство для разработчика: Расширение ядра

Данный раздел предназначен для разработчиков, желающих добавить новые правила анализа или модифицировать существующие. Архитектура ядра спроектирована таким образом, чтобы минимизировать усилия при расширении функционала.

## 1. Структура проекта
Ознакомьтесь с общей архитектурой (см. [Архитектура](architecture.md)). Ключевые файлы для модификации:

- `rules.yaml`: Метаданные правил.
- `checkers.py`: Реализация логики проверки.
- `engine.py`: Подключение новых чекеров.
- `models.py`: Модели данных для `Issue` и `Metric`.

## 2. Добавление нового правила анализа

### Шаг 2.1: Определение метаданных в `rules.yaml`
Добавьте новую запись в список `rules` в файле `rules.yaml`. Присвойте уникальный `id` (например, `STU-PY-07`), укажите `name`, `description`, `severity` и `traceability` (CWE, ISO 25010).

**Пример:**

```yaml
# rules.yaml
rules:
  # ... существующие правила ...
  STU-PY-07:
    name: "AvoidGlobalVariables"
    description: "Использование глобальных переменных усложняет отладку и повторное использование кода."
    severity: "MAJOR"
    traceability:
      iso_25010: "Maintainability"
```

### Шаг 2.2: Реализация логики проверки в checkers.py
Создайте новый класс-чекер или добавьте метод в существующий, наследуемый от BaseChecker.

### Вариант А: Добавление метода в существующий чекер
Если ваше правило логически относится к уже существующему чекеру (например, новое правило именования в NamingChecker).

### Вариант Б: Создание нового класса-чекера
Если правило значительно отличается по функционалу.

1. Создайте новый класс, наследуемый от BaseChecker.
2. Реализуйте необходимые методы visit_XYZ(self, node), где XYZ — это тип AST-узла, который вы хотите анализировать (например, visit_Assign для присваиваний, visit_Call для вызовов функций и т.д.).
3. При обнаружении нарушения вызовите self.report(node, "ВАШ_ID_ПРАВИЛА").
4. Если чекер собирает метрики, добавьте список self.metrics = [] в __init__ и заполняйте его кортежами (metric_name, value, entity). Если нужно собрать метрики после полного обхода, добавьте метод finalize_metrics().

### Пример нового чекера для глобальных переменных:

```Python
# checkers.py
from models import Issue
import ast

class GlobalVariableChecker(BaseChecker):
    """Проверяет использование глобальных переменных."""
    def visit_Assign(self, node):
        # Если присваивание происходит в глобальной области видимости
        if isinstance(node.targets, ast.Name) and isinstance(node.targets.ctx, ast.Store):
            if hasattr(node, 'scope') and isinstance(node.scope, ast.Module): # Псевдо-логика для иллюстрации
                self.report(node, "STU-PY-07")
        self.generic_visit(node)```
*(Примечание: корректное определение глобальной области видимости требует более сложного анализа контекста или использования сторонних библиотек, это лишь иллюстрация.)*
```

### Шаг 2.3: Регистрация нового чекера в `engine.py`
Добавьте ваш новый класс-чекер в список `self.checker_classes` в конструкторе `AnalyzerEngine`.

```python
# engine.py
from checkers import (
    # ... существующие чекеры ...
    GlobalVariableChecker # Новый чекер
)

class AnalyzerEngine:
    def __init__(self, rules_list: list):
        # ...
        self.checker_classes = [
            NamingChecker, 
            ComplexityChecker, 
            ExceptionChecker, 
            ResourceChecker,
            PathChecker,
            CodeVolumeChecker,
            GlobalVariableChecker # Добавьте сюда
        ]
        # ...
```

## Формат ответа (Response Body)
API возвращает JSON-объект, содержащий run_id (идентификатор запуска в БД), общее количество total_issues, список issues (найденных нарушений) и список metrics (собранных количественных показателей).

```JSON
{
  "run_id": 123,
  "total_issues": 3,
  "issues": [
    {
      "rule_id": "STU-PY-01",
      "message": "Использование open() без контекстного менеджера 'with'.",
      "line": 2,
      "severity": "MAJOR"
    },
    {
      "rule_id": "STU-PY-02",
      "message": "Пустой блок except (Silent Exception) подавляет ошибки.",
      "line": 5,
      "severity": "MAJOR"
    },
    {
      "rule_id": "STU-PY-04",
      "message": "Имя функции 'my_bad_func' нарушает PEP8 (используйте snake_case).",
      "line": 1,
      "severity": "MINOR"
    }
  ],
  "metrics": [
    {
      "name": "LinesOfCode",
      "value": 6.0,
      "entity": "Global"
    },
    {
      "name": "CyclomaticComplexity",
      "value": 4.0,
      "entity": "my_bad_func"
    }
  ]
}
```