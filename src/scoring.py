from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    points: int
    grade: str
    reasons: list[str]


def _grade(points: int) -> str:
    if points >= 90:
        return "A"
    if points >= 75:
        return "B"
    if points >= 60:
        return "C"
    if points >= 45:
        return "D"
    return "F"


def score_project(
    docstring_ratio: float, max_complexity: int, duplication_ratio: float
) -> Score:
    penalties: list[tuple[int, str]] = []

    # Docstrings
    if docstring_ratio < 0.5:
        penalties.append(
            (25, "Low docstring coverage (< 50%). Add docstrings to functions/classes.")
        )
    elif docstring_ratio < 0.8:
        penalties.append((10, "Docstring coverage could be improved (50–80%)."))

    # Complexity
    if max_complexity >= 15:
        penalties.append(
            (30, "High cyclomatic-like complexity (>= 15). Refactor large functions.")
        )
    elif max_complexity >= 10:
        penalties.append((15, "Moderate complexity (10–14). Consider splitting logic."))

    # Duplication
    if duplication_ratio >= 0.15:
        penalties.append(
            (20, "Noticeable code duplication (>= 15%). Extract common helpers.")
        )
    elif duplication_ratio >= 0.07:
        penalties.append(
            (10, "Some code duplication (7–15%). Consider refactoring repeated blocks.")
        )

    points = 100 - sum(p for p, _ in penalties)
    points = max(0, min(100, points))

    reasons = [r for _, r in penalties] or [
        "Good overall quality for the selected metrics."
    ]
    return Score(points=points, grade=_grade(points), reasons=reasons)
