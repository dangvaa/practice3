# Student Code Quality Analyzer Core

Ядро системы статического анализа качества кода для студенческих работ на языке Python.

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://dangvaa.github.io/practice3/)

## Основные возможности

- **AST-анализ**: Глубокий анализ структуры кода без его выполнения.
- **Плагинная архитектура**: Легкое добавление новых проверок через наследование классов-чекеров.
- **Хранение в БД**: Результаты каждого запуска сохраняются в PostgreSQL для отслеживания прогресса студента.

## Технологический стек

- **Язык**: Python 3.11+
- **Парсер**: Модуль `ast`
- **БД**: PostgreSQL
- **Конфигурация**: YAML
- **Тестирование**: Pytest

## Реализованные правила

| ID | Название | Описание |
| :--- | :--- | :--- |
| **STU-PY-01** | MissingContextManager | Открытие файлов без менеджера контекста `with`. |
| **STU-PY-02** | SilentException | Подавление исключений через пустой `except: pass` (CWE-391). |
| **STU-PY-03** | HighCyclomaticComplexity | Контроль цикломатической сложности функций (McCabe > 10). |
| **STU-PY-04** | NamingConventionViolation | Проверка именования по PEP 8 (`snake_case` / `PascalCase`). |
| **STU-PY-05** | MissingDocstring | Проверка наличия строк документации (Docstrings). |
| **STU-PY-06** | HardcodedAbsolutePath | Поиск захардкоженных абсолютных путей (CWE-73). |

## Подробная документация доступна по ссылке:  
 [Документация](https://dangvaa.github.io/practice3/)