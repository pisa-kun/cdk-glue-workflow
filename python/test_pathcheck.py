import pytest

from pathcheck import is_targetpath, translated_path

## s3はlinux系なので、本番ではパスの区切り文字が/であることに注意
@pytest.mark.parametrize(('path', 'expected'), [
    ('Test/test/yyyy/MM/dd/test_3333_20230108.csv.gz', True),
    ('Test/test_Load/yyyy/MM/dd/hoge_3333_20230108.csv.gz', False),
    ('Test/test_Moved/yyyy/MM/dd/hoge_3333_20230108.csv.gz', False),
    ('Hoge/test_Raw/yyyy/MM/dd/hoge_3333_20230108.csv.gz', False),
    ('Test/test_Raw/hoge_3333_20230108.csv.gz', False),
    ('Test/test_Raw/yyyy/MM/dd/hoge_3333_20230108.tsv', False),
    ('Test/hoge/yyyy/MM/dd/hoge_3333_20230108.tsv', False),
    ('Test/hoge/yyyy/MM/dd/hoge_3333_20230108.csv.gz', True),
    ('Test/test/yyyy/MM/dd/hoge_3333_20230108.csv', False),
    ('Test/test/yyyy/MM/dd/test_20230108_3333.csv.gz', False),
    ('Test/tamago/yyyy/MM/dd/tamago_3333_20230108.csv.gz',True),
    ('Test/', False),
    ('Test', False),
    ('Test/Test_Raw/', False),
])
def test_is_targetpath(path: str, expected: bool):
    assert is_targetpath(path) == expected

@pytest.mark.parametrize(('path', 'result_expected', 'dest_expected', 'moved_expected', 'error_expected'), [
    ('Test/hoge/yyyy/MM/dd/hoge_3333_20230108.csv.gz',
    True,
    'Test/hoge_Load/yyyy/MM/dd/hoge_3333_20230108.parquet',
    'Test/hoge_Moved/yyyy/MM/dd/hoge_3333_20230108.csv.gz',
    'Test/hoge_Error/yyyy/MM/dd/hoge_3333_20230108.csv.gz'),
    ('Test/hoge/hoge_3333_20230108.csv.gz',False,'','',''),
    ('Test/hoge/yyyy/MM/hoge_3333_20230108.csv.gz',False,'','',''),
    ('Test/test/yyyy/MM/hoge_3333_20230108.csv.gz',False,'','',''),
    ('Test/test/yyyy/MM/dd/test_3333_20230108.csv.gz',
    True,
    'Test/test_Load/yyyy/MM/dd/test_3333_20230108.parquet',
    'Test/test_Moved/yyyy/MM/dd/test_3333_20230108.csv.gz',
    'Test/test_Error/yyyy/MM/dd/test_3333_20230108.csv.gz'),
    ('Test/tamago/yyyy/MM/dd/tamago_3333_20230108.csv.gz',
    True,
    'Test/tamago_Load/yyyy/MM/dd/tamago_3333_20230108.parquet',
    'Test/tamago_Moved/yyyy/MM/dd/tamago_3333_20230108.csv.gz',
    'Test/tamago_Error/yyyy/MM/dd/tamago_3333_20230108.csv.gz'),
    ('Test/tamago/yyyy/dd/tamago_3333_20230108.csv.gz',False, '', '',''),
    ('Test/tamago/yyyy/MM/dd/hoge_3333_20230108.csv.gz',False,'', '',''),
    ('Test/tamago/yyyy/MM/dd/namako_3333_20230108.csv.gz',False,'','',''),
    ('Test/namako/yyyy/MM/dd/namako_3333_20230108.csv.gz',False,'','',''),
    ('Test/tamago/yyyy/MM/dd/tamago_20230108.csv.gz',False,'','',''),
    ('Test/tamago/yyyy/MM/dd/tamago_20230108_3333.csv.gz',False,'','',''),
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