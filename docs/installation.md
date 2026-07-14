# Установка и развертывание

Для развертывания ядра анализатора на вашей локальной машине или сервере выполните следующие шаги.

## 1. Клонирование репозитория

```bash
git clone https://github.com/dangvaa/practice3.git
cd practice3
```

## 2. Настройка базы данных PostgreSQL

1. Убедитесь, что у вас установлен и запущен PostgreSQL.
2. Создайте новую базу данных для анализатора:
   
```sql
SQL CREATE DATABASE analyzer_db;
```

3. Отредактируйте файл .env (см. шаг 3) с учетными данными для доступа к этой базе данных.


## 3. Конфигурация переменных окружения (.env)
Создайте файл .env в корневой директории проекта (analyzer_core/) и заполните его следующими данными. Этот файл не должен попасть в систему контроля версий (Git)!
Пример .env:

```python
DB_NAME=analyzer_db
DB_USER=postgres
DB_PASSWORD=ваш_пароль_от_postgres
DB_HOST=localhost
DB_PORT=5432
```

## 4. Установка зависимостей Python
Создайте виртуальное окружение и установите необходимые библиотеки:

```bash
python -m venv venv
source venv/bin/activate # Для Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 5. Инициализация таблиц базы данных
При первом запуске анализатора таблицы будут созданы автоматически. Вы также можете принудительно инициализировать их, вызвав DbManager:

```bash
# Запустите файл
from database import DbManager
db_manager = DbManager()
print("Таблицы БД успешно инициализированы.")
```

## 6. Запуск анализатора
Чтобы проанализировать файл, используйте main.py:
```bash
python main.py path/to/student_code.py
```

Пример:
```bash
python main.py student_lab.py
```

## 7. Запуск API
Если вы используете API, запустите его с помощью uvicorn:

```bash
uvicorn api:app --reload
```
