from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class DocstringStats:
    total_defs: int
    with_docstring: int

    @property
    def ratio(self) -> float:
        if self.total_defs == 0:
            return 1.0
        return self.with_docstring / self.total_defs


def docstring_stats_for_source(source_code: str) -> DocstringStats:
    tree = ast.parse(source_code)

    total = 0
    with_doc = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total += 1
            if ast.get_docstring(node):
                with_doc += 1

    return DocstringStats(total_defs=total, with_docstring=with_doc)
