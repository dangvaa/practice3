from dataclasses import dataclass

@dataclass
class Issue:
    rule_id: str
    message: str
    line: int
    column: int
    severity: str