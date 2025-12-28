from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.discovery import discover_student_projects
from src.metrics.complexity import complexity_stats_for_source
from src.metrics.docstrings import docstring_stats_for_source
from src.metrics.duplication import duplication_stats_for_source
from src.report import StudentResult, build_json_report, build_markdown_report
from src.scoring import score_project


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess code quality for student submissions.")
    parser.add_argument("--input", required=True, help="Path to folder with student subfolders.")
    parser.add_argument("--out", default="out", help="Output directory for reports.")
    args = parser.parse_args()

    projects = discover_student_projects(args.input)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    results: list[StudentResult] = []

    for project in projects:
        all_text = "\n\n".join(_read_text(p) for p in project.py_files)

        doc_stats = docstring_stats_for_source(all_text)
        c_stats = complexity_stats_for_source(all_text)
        d_stats = duplication_stats_for_source(all_text)

        score = score_project(
            docstring_ratio=doc_stats.ratio,
            max_complexity=c_stats.max_complexity,
            duplication_ratio=d_stats.ratio,
        )

        results.append(
            StudentResult(
                student_id=project.student_id,
                files=len(project.py_files),
                docstring_ratio=doc_stats.ratio,
                max_complexity=c_stats.max_complexity,
                duplication_ratio=d_stats.ratio,
                points=score.points,
                grade=score.grade,
                reasons=score.reasons,
            )
        )

    json_report = build_json_report(results)
    (out_dir / "report.json").write_text(json.dumps(json_report, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "report.md").write_text(build_markdown_report(results), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
