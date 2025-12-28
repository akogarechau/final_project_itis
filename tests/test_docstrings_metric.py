from src.metrics.docstrings import docstring_stats_for_source


def test_docstring_ratio() -> None:
    code = '''
def a():
    """doc"""
    return 1

def b():
    return 2
'''
    stats = docstring_stats_for_source(code)
    assert stats.total_defs == 2
    assert stats.with_docstring == 1
    assert 0.4 < stats.ratio < 0.6
