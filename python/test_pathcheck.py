import pytest

from pathcheck import is_targetpath, translated_path

@pytest.mark.parametrize(('path', 'expected'), [
    ('Test/Test-Raw/yyyy/MM/dd/hoge-yyyyMMdd.csv', True),
    ('Test/Test-Load/yyyy/MM/dd/hoge-yyyyMMdd.csv', True),
    ('Test/Test-Moved/yyyy/MM/dd/hoge-yyyyMMdd.csv', True),
    ('Hoge/Test-Raw/yyyy/MM/dd/hoge-yyyyMMdd.csv', True),
    ('Test/Test-Raw/hoge-yyyyMMdd.csv', True),
    ('Test/Test-Raw/yyyy/MM/dd/hoge-yyyyMMdd.tsv', True),
])
def test_is_targetpath(path: str, expected: bool):
    assert is_targetpath(path) == expected

@pytest.mark.parametrize(('path', 'dest_expected', 'dest_moved'), [
    ('Test/Test-Raw/yyyy/MM/dd/hoge-yyyyMMdd.csv', 'testA', 'testB'),
])
def test_translated_path(path: str, dest_expected: str, dest_moved: str):
    assert translated_path(path) == (dest_expected, dest_moved)