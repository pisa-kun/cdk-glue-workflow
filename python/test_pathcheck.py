import pytest

from pathcheck import is_targetpath, translated_path

## s3はlinux系なので、本番ではパスの区切り文字が/であることに注意
@pytest.mark.parametrize(('path', 'expected'), [
    ('Test/test/yyyy/MM/dd/test-3333-20230108.csv.gz', True),
    ('Test/test-Load/yyyy/MM/dd/hoge-3333-20230108.csv.gz', False),
    ('Test/test-Moved/yyyy/MM/dd/hoge-3333-20230108.csv.gz', False),
    ('Hoge/test-Raw/yyyy/MM/dd/hoge-3333-20230108.csv.gz', False),
    ('Test/test-Raw/hoge-3333-20230108.csv.gz', False),
    ('Test/test-Raw/yyyy/MM/dd/hoge-3333-20230108.tsv', False),
    ('Test/hoge/yyyy/MM/dd/hoge-3333-20230108.tsv', False),
    ('Test/hoge/yyyy/MM/dd/hoge-3333-20230108.csv.gz', True),
    ('Test/test/yyyy/MM/dd/hoge-3333-20230108.csv', False),
    ('Test/test/yyyy/MM/dd/test-20230108-3333.csv.gz', False),
    ('Test/tamago/yyyy/MM/dd/tamago-3333-20230108.csv.gz',True),
    ('Test/', False),
    ('Test', False),
    ('Test/Test-Raw/', False),
])
def test_is_targetpath(path: str, expected: bool):
    assert is_targetpath(path) == expected

@pytest.mark.parametrize(('path', 'result_expected', 'dest_expected', 'moved_expected', 'error_expected'), [
    ('Test/hoge/yyyy/MM/dd/hoge-3333-20230108.csv.gz',
    True,
    'Test/hoge-Load/yyyy/MM/dd/hoge-3333-20230108.parquet',
    'Test/hoge-Moved/yyyy/MM/dd/hoge-3333-20230108.csv.gz',
    'Test/hoge-Error/yyyy/MM/dd/hoge-3333-20230108.csv.gz'),
    ('Test/hoge/hoge-3333-20230108.csv.gz',False,'','',''),
    ('Test/hoge/yyyy/MM/hoge-3333-20230108.csv.gz',False,'','',''),
    ('Test/test/yyyy/MM/hoge-3333-20230108.csv.gz',False,'','',''),
    ('Test/test/yyyy/MM/dd/test-3333-20230108.csv.gz',
    True,
    'Test/test-Load/yyyy/MM/dd/test-3333-20230108.parquet',
    'Test/test-Moved/yyyy/MM/dd/test-3333-20230108.csv.gz',
    'Test/test-Error/yyyy/MM/dd/test-3333-20230108.csv.gz'),
    ('Test/tamago/yyyy/MM/dd/tamago-3333-20230108.csv.gz',
    True,
    'Test/tamago-Load/yyyy/MM/dd/tamago-3333-20230108.parquet',
    'Test/tamago-Moved/yyyy/MM/dd/tamago-3333-20230108.csv.gz',
    'Test/tamago-Error/yyyy/MM/dd/tamago-3333-20230108.csv.gz'),
    ('Test/tamago/yyyy/dd/tamago-3333-20230108.csv.gz',False, '', '',''),
    ('Test/tamago/yyyy/MM/dd/hoge-3333-20230108.csv.gz',False,'', '',''),
    ('Test/tamago/yyyy/MM/dd/namako-3333-20230108.csv.gz',False,'','',''),
    ('Test/namako/yyyy/MM/dd/namako-3333-20230108.csv.gz',False,'','',''),
    ('Test/tamago/yyyy/MM/dd/tamago-20230108.csv.gz',False,'','',''),
    ('Test/tamago/yyyy/MM/dd/tamago-20230108-3333.csv.gz',False,'','',''),
])
def test_translated_path(path: str, result_expected: bool, dest_expected: str, moved_expected: str, error_expected: str):
    result, paths = translated_path(path)

    assert result == result_expected
    if result:
        assert paths.dest == dest_expected
        assert paths.moved == moved_expected
        assert paths.error == error_expected
    else:
        assert paths == None