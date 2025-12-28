from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    points: int
    grade: str
    reasons: list[str]


def score_project(
    docstring_ratio: float,
    max_complexity: int,
    duplication_ratio: float,
) -> Score:
    # MVP scoring: 0..100 points
    points = 100
    reasons: list[str] = []

    # Docstrings
    if docstring_ratio < 0.5:
        points -= 25
        reasons.append("Low docstring coverage (< 50%). Add docstrings to functions/classes.")
    elif docstring_ratio < 0.8:
        points -= 10
        reasons.append("Docstring coverage could be improved (50–80%).")

    # Complexity
    if max_complexity >= 15:
        points -= 30
        reasons.append("High cyclomatic-like complexity (>= 15). Refactor large functions.")
    elif max_complexity >= 10:
        points -= 15
        reasons.append("Moderate complexity (10–14). Consider splitting logic.")

    # Duplication
    if duplication_ratio >= 0.15:
        points -= 20
        reasons.append("Noticeable code duplication (>= 15%). Extract common helpers.")
    elif duplication_ratio >= 0.07:
        points -= 10
        reasons.append("Some code duplication (7–15%). Consider refactoring repeated blocks.")

    points = max(0, min(100, points))

    if points >= 90:
        grade = "A"
    elif points >= 75:
        grade = "B"
    elif points >= 60:
        grade = "C"
    elif points >= 45:
        grade = "D"
    else:
        grade = "F"

    if not reasons:
        reasons.append("Good overall quality for the selected metrics.")

    return Score(points=points, grade=grade, reasons=reasons)
