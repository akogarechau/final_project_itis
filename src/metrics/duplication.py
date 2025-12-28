from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class DuplicationStats:
    duplicated_lines: int
    total_lines: int
    unique_lines: int

    @property
    def duplication_ratio(self) -> float:
        if self.total_lines == 0:
            return 0.0
        return self.duplicated_lines / self.total_lines

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["duplication_ratio"] = self.duplication_ratio
        return data

    # Если где-то в коде ожидают "как словарь"
    def __getitem__(self, key: str) -> Any:
        return self.to_dict()[key]


def _is_ignorable_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.startswith("#"):
        return True
    return False


def _normalize_line(line: str) -> str:
    # Нормализация для сравнения: убираем крайние пробелы и схлопываем внутренние.
    s = " ".join(line.strip().split())
    return s


def duplication_stats_for_source(
    source_code: str, *, min_line_len: int = 12
) -> DuplicationStats:
    """
    Простейшая метрика дублирования для одного исходника.

    Идея:
    - берём строки кода,
    - выкидываем пустые/комментарии,
    - нормализуем пробелы,
    - считаем строку "дублирующейся", если она встречается 2+ раз (и достаточно длинная).
    """
    raw_lines = source_code.splitlines()

    normalized_lines: list[str] = []
    for line in raw_lines:
        if _is_ignorable_line(line):
            continue
        normalized_lines.append(_normalize_line(line))

    total = len(normalized_lines)

    seen: set[str] = set()
    duplicates = 0

    for line in normalized_lines:
        if len(line) < min_line_len:
            # короткие строки типа "pass", "return x" часто дают шум — их игнорируем
            continue
        if line in seen:
            duplicates += 1
