import pytest

from pathcheck import is_targetpath, translated_path

## s3はlinux系なので、本番ではパスの区切り文字が/であることに注意
@pytest.mark.parametrize(('path', 'expected'), [
    ('Test/Test-Raw/yyyy/MM/dd/hoge-20230108.csv.gz', True),
    ('Test/Test-Load/yyyy/MM/dd/hoge-20230108.csv.gz', False),
    ('Test/Test-Moved/yyyy/MM/dd/hoge-20230108.csv.gz', False),
    ('Hoge/Test-Raw/yyyy/MM/dd/hoge-20230108.csv.gz', False),
    ('Test/Test-Raw/hoge-20230108.csv.gz', False),
    ('Test/Test-Raw/yyyy/MM/dd/hoge-20230108.tsv', False),
    ('Test/Test-Raw/yyyy/MM/dd/hoge-20230108.csv', False),
    ('Test/', False),
    ('Test', False),
    ('Test/Test-Raw/', False),
])
def test_is_targetpath(path: str, expected: bool):
    assert is_targetpath(path) == expected

@pytest.mark.parametrize(('path', 'dest_expected', 'moved_expected', 'error_expected'), [
    ('Test/hoge/yyyy/MM/dd/hoge-20230108.csv.gz',
    'Test/hoge-Load/yyyy/MM/dd/hoge-20230108.parquet',
    'Test/hoge-Moved/yyyy/MM/dd/hoge-20230108.csv.gz',
    'Test/hoge-Error/yyyy/MM/dd/hoge-20230108.csv.gz'),
    ('Test/hoge/hoge-20230108.csv.gz','','',''),
    ('Test/hoge/yyyy/MM/hoge-20230108.csv.gz','','',''),
    ('Test/test/yyyy/MM/hoge-20230108.csv.gz','','',''),
    ('Test/test/yyyy/MM/dd/test-20230108.csv.gz',
    'Test/test-Load/yyyy/MM/dd/test-20230108.parquet',
    'Test/test-Moved/yyyy/MM/dd/test-20230108.csv.gz',
    'Test/test-Error/yyyy/MM/dd/test-20230108.csv.gz'),
    ('Test/tamago/yyyy/MM/dd/tamago-20230108.csv.gz',
    'Test/tamago-Load/yyyy/MM/dd/tamago-20230108.parquet',
    'Test/tamago-Moved/yyyy/MM/dd/tamago-20230108.csv.gz',
    'Test/tamago-Error/yyyy/MM/dd/tamago-20230108.csv.gz'),
    ('Test/tamago/yyyy/dd/tamago-20230108.csv.gz', "", "",''),
    ('Test/tamago/yyyy/MM/dd/hoge-20230108.csv.gz','', '',''),
    ('Test/tamago/yyyy/MM/dd/namako-20230108.csv.gz','','',''),
    ('Test/namako/yyyy/MM/dd/namako-20230108.csv.gz','','',''),
    ('Test/tamago/yyyy/MM/dd/tamago.csv.gz','','',''),
])
def test_translated_path(path: str, dest_expected: str, moved_expected: str, error_expected: str):
    dest, moved, error = translated_path(path)
    assert dest == dest_expected
    assert moved == moved_expected
    assert error == error_expected