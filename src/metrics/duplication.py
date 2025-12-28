from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DuplicationStats:
    duplicated_lines: int
    total_lines: int

    @property
    def ratio(self) -> float:
        """Duplicated / total (0..1)."""
        if self.total_lines <= 0:
            return 0.0
        return self.duplicated_lines / self.total_lines


def duplication_stats_for_source(
    source_code: str, *, min_line_len: int = 12
) -> DuplicationStats:
    """
    Very simple duplication metric for a single source file.

    Rules:
    - Ignore empty lines and comments (# ...)
    - Normalize spaces
    - A line counts as duplicated if it appears more than once (and length >= min_line_len)
    """
    try:
        if source_code is None:
            source_code = ""
        if not isinstance(source_code, str):
            source_code = str(source_code)

        raw_lines = source_code.splitlines()

        normalized: list[str] = []
        for line in raw_lines:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            s = " ".join(s.split())
            normalized.append(s)

        total = len(normalized)
        if total == 0:
            return DuplicationStats(duplicated_lines=0, total_lines=0)

        seen: set[str] = set()
        duplicated = 0

        for line in normalized:
            if len(line) < min_line_len:
                continue
            if line in seen:
                duplicated += 1
            else:
                seen.add(line)

        return DuplicationStats(duplicated_lines=duplicated, total_lines=total)

    except Exception:
        # Never break report generation because of duplication metric.
        return DuplicationStats(duplicated_lines=0, total_lines=0)
