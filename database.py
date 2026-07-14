import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DbManager:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "analyzer_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
            )
            self._bootstrap()
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def _bootstrap(self):
        """Создание таблиц"""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS projects (id SERIAL PRIMARY KEY, name TEXT UNIQUE);
                CREATE TABLE IF NOT EXISTS analysis_runs (
                    id SERIAL PRIMARY KEY, 
                    project_id INTEGER REFERENCES projects(id),
                    total_issues INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS issues (
                    id SERIAL PRIMARY KEY,
                    run_id INTEGER REFERENCES analysis_runs(id),
                    rule_id TEXT, message TEXT, line_number INTEGER, severity TEXT
                );
                CREATE TABLE IF NOT EXISTS metrics (
                    id SERIAL PRIMARY KEY,
                    run_id INTEGER REFERENCES analysis_runs(id),
                    name TEXT,
                    value FLOAT,
                    entity TEXT
                );
            """)
            self.conn.commit()

    def save_analysis(self, project_name, issues):
        """Сохранение данных проверки"""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO projects (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id",
                (project_name,),
            )
            p_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO analysis_runs (project_id, total_issues) VALUES (%s, %s) RETURNING id",
                (p_id, len(issues)),
            )
            run_id = cur.fetchone()[0]

            for issue in issues:
                cur.execute(
                    "INSERT INTO issues (run_id, rule_id, message, line_number, severity) VALUES (%s, %s, %s, %s, %s)",
                    (run_id, issue.rule_id, issue.message, issue.line, issue.severity),
                )
            self.conn.commit()
            return run_id

    def save_metrics(self, run_id, metrics_list):
        """
        metrics_list: список кортежей [('Complexity', 12.0, 'my_func'), ...]
        """
        with self.conn.cursor() as cur:
            for m_name, m_value, m_entity in metrics_list:
                cur.execute(
                    "INSERT INTO metrics (run_id, name, value, entity) VALUES (%s, %s, %s, %s)",
                    (run_id, m_name, m_value, m_entity),
                )
            self.conn.commit()
