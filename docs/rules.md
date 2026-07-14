# Реализованные правила анализа

Ядро анализатора проверяет следующие 6 правил, классифицированных по международным стандартам CWE (Common Weakness Enumeration) и ISO 25010 (Product Quality Model).

## 1. STU-PY-01: MissingContextManager
- **Описание:** Использование `open()` без контекстного менеджера `with`. Это может привести к утечке дескрипторов файлов или другим проблемам с ресурсами.
- **Severity:** MAJOR
- **Трассировка:** CWE-772 (Missing Release of Resource), ISO 25010 (Reliability)
- **Пример плохого кода:**

```python
f = open('test.txt', 'w')
f.write('data')
# f.close() отсутствует
```

## 2. STU-PY-02: SilentException
- **Описание:** Пустой блок except: или except Exception: pass подавляет ошибки, затрудняя отладку и скрывая потенциальные проблемы в работе программы.
- **Severity:** MAJOR
- **Трассировка:** CWE-391 (Unchecked Error Condition), ISO 25010 (Reliability)
- **Пример плохого кода:**

```Python
try:
    result = 1 / 0
except:
    pass # Ошибка проглочена
```

## 3. STU-PY-03: HighCyclomaticComplexity
- **Описание:** Слишком высокая цикломатическая сложность функции. Код с высокой сложностью трудно читать, тестировать и поддерживать. Рекомендуется разбить такую функцию на несколько мелких.
- **Severity:** MAJOR
- **Трассировка:** CWE-1076 (Code Complexity), ISO 25010 (Maintainability)
- **Порог:** > 10 (показатель Маккейба)
- **Пример плохого кода:**

```Python
def complex_logic(x, y):
    if x > 0:
        if y > 0:
            for i in range(x):
                while i < y:
                    if x % i == 0:
                        # ... очень много вложенностей ...
                        pass
```

## 4. STU-PY-04: NamingConventionViolation
- **Описание:** Имена функций и переменных не соответствуют стандарту PEP 8 (должны быть в стиле snake_case). Имена классов должны быть в PascalCase.
- **Severity:** MINOR
- **Трассировка:** ISO 25010 (Maintainability)
- **Пример плохого кода:**

```Python
def calculateResults(): # Должно быть calculate_results
    pass
MyVariable = 10 # Должно быть my_variable
```

## 5. STU-PY-05: MissingDocstring
- **Описание:** Отсутствует строка документации (docstring) у публичной функции или класса. Docstrings необходимы для понимания кода другими разработчиками и автоматической генерации документации.
- **Severity:** MINOR
- **Трассировка**: ISO 25010 (Maintainability, Analysability)
- **Пример плохого кода:**

```Python
def my_function():
    # Docstring отсутствует
    pass
```

## 6. STU-PY-06: HardcodedAbsolutePath
- **Описание:** Использование абсолютных путей к файлам или директориям в строковых константах. Это делает программу непереносимой между различными операционными системами или окружениями.
- **Severity:** MAJOR
- **Трассировка:** CWE-73 (External Control of File Name or Path), ISO 25010 (Portability)
- **Пример плохого кода:**

```Python
file_path = "C:/Users/username/data.txt" # Windows
log_dir = "/home/user/logs/"              # Linux
```