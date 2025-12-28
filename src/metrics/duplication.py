from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DuplicationStats:
    duplicated_lines: int
    total_lines: int

    @property
    def ratio(self) -> float:
        if self.total_lines == 0:
            return 0.0
        return self.duplicated_lines / self.total_lines


def duplication_stats_for_source(source_code: str, min_line_len: int = 12) -> DuplicationStats:
    lines_raw = source_code.splitlines()
    normalized: list[str] = []
    for line in lines_raw:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        normalized.append(line)

    seen: set[str] = set()
    duplicated = 0
    for line in normalized:
        if len(line) < min_line_len:
            continue
        if line in seen:
            duplicated += 1
        else:
            seen.add(line)

    return DuplicationStats(duplicated_lines=duplicated, total_lines=len(normalized))
