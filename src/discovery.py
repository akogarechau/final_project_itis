from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StudentProject:
    student_id: str
    root: Path
    py_files: list[Path]


def _is_ignored_dir(path: Path) -> bool:
    name = path.name
    return name in {"__pycache__", ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache", "venv", ".venv"}


def discover_student_projects(input_dir: str | Path) -> list[StudentProject]:
    base = Path(input_dir)
    if not base.exists() or not base.is_dir():
        raise ValueError(f"Input directory does not exist or is not a directory: {base}")

    projects: list[StudentProject] = []
    for student_dir in sorted([p for p in base.iterdir() if p.is_dir()]):
        if student_dir.name.startswith(".") or _is_ignored_dir(student_dir):
            continue

        py_files: list[Path] = []
        for p in student_dir.rglob("*.py"):
            if any(_is_ignored_dir(parent) for parent in p.parents):
                continue
            py_files.append(p)

        projects.append(StudentProject(student_id=student_dir.name, root=student_dir, py_files=sorted(py_files)))

    return projects
