import pandas as pd
from pandas.util.testing import assert_frame_equal
import re
import datetime
import pytest

from dataframe import translate, init_dataframe, translate2

def test_translate():
    expected = pd.DataFrame({
        'format': ['0001', '0001'],
        'serial': ['CFAA123', 'FZAA123'],
        'inputdate': ["2022-11-08 17:54:30", "2022-12-08 17:54:30"],
        'memo': ["0123456790ABCDefパイソン", "xyz789パイソンパイソン"],
    })

    inp = init_dataframe("csv\\test_0001_20221109122531.csv")
    df = translate(inp, 'csv\\test_0001_20221109122531.csv')
    # # 時刻形式を型一致させる
    m2 = re.search(r'\d{14}', 'test_0001_20221109122531.csv')
    t = m2.group()
    expected.insert(1, "time", datetime.datetime.strptime(t, "%Y%m%d%H%M%S"))
    expected['inputdate'] = expected["inputdate"].astype('datetime64')
    df['inputdate'] = df["inputdate"].astype('datetime64')
    print(expected)
    print(df)
    assert_frame_equal(df, expected, check_datetimelike_compat=True)

def test_translate2():
    expected = pd.DataFrame({
        'format': ['0001', '0001','0001'],
        'model': ['CF12345abc', 'FZ12345ABC', 'FZabcd12345'],
        'serial': ['0H888aaaaa', '0000000000', 'abcdef'],
        'data1': ['0123456790ABCDefパイソン', 'xyz789パイソンパイソン', 'xyz789'],
        'data2': ['', '', '0123456790'],
        'flag': [1, 1, 0],
    }, )

    inp = init_dataframe("csv\\hoge_0001_20230111122531.csv")
    df = translate2(inp, 'csv\\hoge_0001_20230111122531.csv')
    # # 時刻形式を型一致させる
    m2 = re.search(r'\d{14}', 'hoge_0001_20230111122531.csv')
    t = m2.group()
    expected.insert(1, "time", datetime.datetime.strptime(t, "%Y%m%d%H%M%S"))
    print(expected)
    print(df)
    assert_frame_equal(df, expected, check_datetimelike_compat=True)

def test_translate_filename_error():
    with pytest.raises(Exception) as e:
        _ = translate('', '')

def test_init_dataframe():
    inp = init_dataframe("csv\\test_0001_20221109122531.csv")
    exp = pd.DataFrame({
        'serial': ['CF-AA123', 'FZ-AA123', 'WX-AA123'],
        'inputdate': ["2022-11-09 02:54:30.000000", "2022-12-09 02:54:30.000000", "2022-13-09 02:54:30.000000"],
        'memo': ["０１２３４56790ＡＢＣＤefパイソン", "xyz789ﾊﾟｲｿﾝﾊﾟｲｿﾝ" , "xyz789"],
    })
    print(inp)
    print(exp)
    assert_frame_equal(inp, exp)