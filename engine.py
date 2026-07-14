import ast
from checkers import (
    NamingChecker,
    ComplexityChecker,
    ExceptionChecker,
    ResourceChecker,
    PathChecker,
    CodeVolumeChecker,
)
from models import Issue


class AnalyzerEngine:
    def __init__(self, rules_metadata: dict):
        self.rules_metadata = rules_metadata
        self.checker_classes = [
            NamingChecker,
            ComplexityChecker,
            ExceptionChecker,
            ResourceChecker,
            PathChecker,
            CodeVolumeChecker,
        ]

    def run(self, code_text):
        """Запуск анализа"""
        try:
            tree = ast.parse(code_text)
            all_issues = []
            all_metrics = []

            for cls in self.checker_classes:
                checker = cls(self.rules_metadata)
                checker.visit(tree)

                if hasattr(checker, "finalize_metrics"):
                    checker.finalize_metrics()

                all_issues.extend(checker.issues)
                if hasattr(checker, "metrics"):
                    all_metrics.extend(checker.metrics)

            return all_issues, all_metrics
        except SyntaxError as e:
            from models import Issue

            return [Issue("SYNTAX", f"Error: {e.msg}", e.lineno, 0, "CRITICAL")], []
