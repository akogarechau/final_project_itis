from __future__ import annotations

import ast
from dataclasses import dataclass


_BRANCH_NODES = (
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.Try,
    ast.With,
    ast.AsyncWith,
    ast.BoolOp,      # and/or
    ast.IfExp,       # ternary
    ast.comprehension,
)


@dataclass(frozen=True)
class ComplexityStats:
    functions: int
    avg_complexity: float
    max_complexity: int


def _function_complexity(fn: ast.AST) -> int:
    # MVP: "cyclomatic-like" complexity = 1 + number of branching nodes inside function
    complexity = 1
    for node in ast.walk(fn):
        if isinstance(node, _BRANCH_NODES):
            complexity += 1
    return complexity


def complexity_stats_for_source(source_code: str) -> ComplexityStats:
    tree = ast.parse(source_code)

    complexities: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            complexities.append(_function_complexity(node))

    if not complexities:
        return ComplexityStats(functions=0, avg_complexity=1.0, max_complexity=1)

    return ComplexityStats(
        functions=len(complexities),
        avg_complexity=sum(complexities) / len(complexities),
        max_complexity=max(complexities),
    )
