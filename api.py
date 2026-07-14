from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from engine import AnalyzerEngine
from database import DbManager
import yaml

app = FastAPI(title="Student Code Quality API")


class AnalysisRequest(BaseModel):
    project_name: str
    code: str


class IssueResponse(BaseModel):
    rule_id: str
    message: str
    line: int
    severity: str


class AnalysisResponse(BaseModel):
    run_id: int
    total_issues: int
    issues: List[IssueResponse]
    metrics: List[Dict]


def load_rules():
    """Загрузка правилл"""
    with open("rules.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("rules", [])


rules_metadata = load_rules()
engine = AnalyzerEngine(rules_metadata)
db = DbManager()


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: AnalysisRequest):
    try:
        issues, metrics = engine.run(request.code)

        run_id = db.save_analysis(request.project_name, issues)
        db.save_metrics(run_id, metrics)

        return {
            "run_id": run_id,
            "total_issues": len(issues),
            "issues": [
                {
                    "rule_id": i.rule_id,
                    "message": i.message,
                    "line": i.line,
                    "severity": i.severity,
                }
                for i in issues
            ],
            "metrics": [{"name": m[0], "value": m[1], "entity": m[2]} for m in metrics],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
