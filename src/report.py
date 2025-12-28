from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class StudentResult:
    student_id: str
    files: int
    docstring_ratio: float
    max_complexity: int
    duplication_ratio: float
    points: int
    grade: str
    reasons: list[str]


def build_json_report(results: list[StudentResult]) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "students": [asdict(r) for r in results],
    }


def build_markdown_report(results: list[StudentResult]) -> str:
    lines: list[str] = []
    lines.append("# Code Quality Report")
    lines.append("")
    lines.append("| Student | Files | Docstrings | Max complexity | Duplication | Points | Grade |")
    lines.append("|---|---:|---:|---:|---:|---:|:---:|")

    for r in results:
        lines.append(
            f"| {r.student_id} | {r.files} | {r.docstring_ratio:.2f} | {r.max_complexity} | "
            f"{r.duplication_ratio:.2f} | {r.points} | {r.grade} |"
        )

    lines.append("")
    lines.append("## Recommendations")
    for r in results:
        lines.append(f"### {r.student_id} ({r.grade}, {r.points})")
        for reason in r.reasons:
            lines.append(f"- {reason}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
