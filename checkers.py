import ast
import re
from models import Issue


class BaseChecker(ast.NodeVisitor):
    """Абстрактный базовый класс для всех чекеров."""

    def __init__(self, rules_list: list):
        """Инициализация базового чекера."""
        super().__init__()
        self.rules_metadata = {rule["id"]: rule for rule in rules_list}
        self.issues = []

    def report(self, node, rule_id):
        """Зарегистрировать нарушение правила."""
        rule_info = self.rules_metadata.get(rule_id, {})
        self.issues.append(
            Issue(
                rule_id=rule_id,
                message=rule_info.get("description", "No description"),
                line=getattr(node, "lineno", 0),
                column=getattr(node, "col_offset", 0),
                severity=rule_info.get("severity", "INFO"),
            )
        )


class NamingChecker(BaseChecker):
    """Отвечает за проверку именования и расчет метрик документированности."""

    SNAKE_CASE_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*$")
    PASCAL_CASE_PATTERN = re.compile(r"^[A-Z][a-zA-Z0-9]*$")

    def __init__(self, rules_list):
        super().__init__(rules_list)
        self.metrics = []
        self.total_functions = 0
        self.documented_functions = 0
        self.total_classes = 0
        self.documented_classes = 0

    def visit_FunctionDef(self, node):
        """Проверяет docstring у функции"""
        self.total_functions += 1
        if not self.SNAKE_CASE_PATTERN.match(node.name):
            self.report(node, "STU-PY-04")
        doc = ast.get_docstring(node)
        if not doc:
            self.report(node, "STU-PY-05")
        else:
            self.documented_functions += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Проверяет docstring у классов"""
        self.total_classes += 1
        if not self.PASCAL_CASE_PATTERN.match(node.name):
            self.report(node, "STU-PY-04")
        doc = ast.get_docstring(node)
        if not doc:
            self.report(node, "STU-PY-05")
        else:
            self.documented_classes += 1
        self.generic_visit(node)

    def finalize_metrics(self):
        """Вычисляет итоговые метрики по документации и количеству объектов."""
        self.metrics.append(("FunctionCount", float(self.total_functions), "Global"))
        self.metrics.append(("ClassCount", float(self.total_classes), "Global"))

        if self.total_functions > 0:
            f_coverage = (self.documented_functions / self.total_functions) * 100
            self.metrics.append(("FunctionDocCoverage", float(f_coverage), "Global"))

        if self.total_classes > 0:
            c_coverage = (self.documented_classes / self.total_classes) * 100
            self.metrics.append(("ClassDocCoverage", float(c_coverage), "Global"))

        total_entities = self.total_functions + self.total_classes
        documented_entities = self.documented_functions + self.documented_classes

        if total_entities > 0:
            total_coverage = (documented_entities / total_entities) * 100
            self.metrics.append(("TotalDocCoverage", float(total_coverage), "Global"))


class ComplexityChecker(BaseChecker):
    """Отвечает за расчет цикломатической сложности."""

    def __init__(self, rules_metadata):
        """Инициализация чекера сложности."""
        super().__init__(rules_metadata)
        self.metrics = []

    def visit_FunctionDef(self, node):
        """Вычисляет цикломатическую сложность функции."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(
                child,
                (
                    ast.If,
                    ast.For,
                    ast.While,
                    ast.ExceptHandler,
                    ast.With,
                    ast.IfExp,
                    ast.BoolOp,
                ),
            ):
                complexity += 1

        self.metrics.append(("CyclomaticComplexity", float(complexity), node.name))

        if complexity > 10:
            self.report(node, "STU-PY-03")

        self.generic_visit(node)


class ExceptionChecker(BaseChecker):
    """Отвечает за проверку обработки исключений."""

    def visit_ExceptHandler(self, node):
        """Проверяет, что блок except не пустой."""
        if not node.body or (
            len(node.body) == 1 and isinstance(node.body[0], ast.Pass)
        ):
            self.report(node, "STU-PY-02")
        self.generic_visit(node)


class ResourceChecker(BaseChecker):
    """Отвечает за безопасную работу с ресурсами (файлами)."""

    def __init__(self, rules_metadata):
        """Инициализация чекера ресурсов."""
        super().__init__(rules_metadata)
        self._in_with = False

    def visit_With(self, node):
        """Отслеживает вход в блок with."""
        self._in_with = True
        self.generic_visit(node)
        self._in_with = False

    def visit_Call(self, node):
        """Проверяет вызовы open() на нахождение внутри with."""
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            if not self._in_with:
                self.report(node, "STU-PY-01")
        self.generic_visit(node)


class PathChecker(BaseChecker):
    """Отвечает за поиск абсолютных путей в коде."""

    def visit_Constant(self, node):
        """Проверяет строковые константы на наличие абсолютных путей."""
        if isinstance(node.value, str):
            if re.search(
                r"^[a-zA-Z]:\\|^[a-zA-Z]:/|^/home/|^/Users/", node.value, re.IGNORECASE
            ):
                self.report(node, "STU-PY-06")
        self.generic_visit(node)


class CodeVolumeChecker(BaseChecker):
    """Сбор количественных метрик объема исходного кода."""

    def __init__(self, rules_list):
        """Инициализация чекера объема кода."""
        super().__init__(rules_list)
        self.metrics = []

    def visit_Module(self, node):
        """Вычисляет количество строк кода в модуле."""
        loc = 0
        if hasattr(node, "end_lineno") and node.end_lineno:
            loc = node.end_lineno
        else:
            loc = max((getattr(n, "lineno", 0) for n in ast.walk(node)), default=0)

        self.metrics.append(("LinesOfCode", float(loc), "Global"))
        self.generic_visit(node)
