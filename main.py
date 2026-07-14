import yaml
import os
import argparse
from dotenv import load_dotenv
from engine import AnalyzerEngine
from database import DbManager

load_dotenv()

def load_rules(path="rules.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("rules", [])


def main():
    parser = argparse.ArgumentParser(description="Ядро анализатора качества кода")
    parser.add_argument("file", help="Путь к файлу Python для анализа")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Ошибка: Файл {args.file} не найден.")
        return

    rules_metadata = load_rules()
    engine = AnalyzerEngine(rules_metadata)
    db = DbManager() 

    print(f"Анализ файла: {args.file}")
    with open(args.file, "r", encoding="utf-8") as f:
        code = f.read()

    issues, metrics = engine.run(code)
    project_name = os.path.basename(args.file)
    run_id = db.save_analysis(project_name, issues)

    if metrics:
        db.save_metrics(run_id, metrics)
        print(f" Сохранено метрик: {len(metrics)}")

    print(f"\nУспех! Run ID: {run_id}")
    print(f"Всего ошибок: {len(issues)}")

    if issues:
        print("Детальный список нарушений:")
        for i in issues:
            print(f"  - Line {i.line}: [{i.rule_id}] {i.message}")

    if metrics:
        print("Собранные метрики кода:")
        for m_name, m_val, m_entity in metrics:
            print(f"  - {m_entity} -> {m_name}: {m_val}")


if __name__ == "__main__":
    main()
