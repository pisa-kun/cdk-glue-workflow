import pytest

from pathcheck import is_targetpath, translated_path

## s3はlinux系なので、本番ではパスの区切り文字が/であることに注意
@pytest.mark.parametrize(('path', 'expected'), [
    ('Test\Test-Raw\yyyy\MM\dd\hoge-yyyyMMdd.csv', True),
    ('Test\Test-Load\yyyy\MM\dd\hoge-yyyyMMdd.csv', False),
    ('Test\Test-Moved\yyyy\MM\dd\hoge-yyyyMMdd.csv', False),
    ('Hoge\Test-Raw\yyyy\MM\dd\hoge-yyyyMMdd.csv', False),
    ('Test\Test-Raw\hoge-yyyyMMdd.csv', False),
    ('Test\Test-Raw\yyyy\MM\dd\hoge-yyyyMMdd.tsv', False),
])
def test_is_targetpath(path: str, expected: bool):
    assert is_targetpath(path) == expected

@pytest.mark.parametrize(('path', 'dest_expected', 'moved_expected'), [
    ('Test\Test-Raw\yyyy\MM\dd\hoge-yyyyMMdd.csv',
    'Test\Test-Load\yyyy\MM\dd\hoge-yyyyMMdd.csv',
    'Test\Test-Moved\yyyy\MM\dd\hoge-yyyyMMdd.csv'),
    ('Test\Test-Raw\hoge-yyyyMMdd.csv','',''),
])
def test_translated_path(path: str, dest_expected: str, moved_expected: str):
    assert translated_path(path) == (dest_expected, moved_expected)