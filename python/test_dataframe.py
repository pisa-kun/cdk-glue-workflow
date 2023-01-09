import pandas as pd
from pandas.util.testing import assert_frame_equal
import re
import datetime

from dataframe import initialize, translate, init_dataframe

# df = pd.DataFrame({
#     'name': ['rinze', 'natsuha', 'juri', 'kaho', 'chiyoko'],
#     'age': [16, 20, 17, 12, 17],
#     'theme': ['blue', 'green', 'yellow', None , 'pink'],
# })

# def test_initialize():
#     assert_frame_equal(initialize(), df)

def test_translate():
    expected = pd.DataFrame({
        'format': ['0001', '0001'],
        'serial': ['CFAA123', 'FZAA123'],
        'inputdate': ["2022-11-08 17:54:30", "2022-12-08 17:54:30"],
        'memo': ["0123456790ABCDefパイソン", "xyz789パイソンパイソン"],
    })

    inp = init_dataframe("csv\\test_0001_20221109122531.csv")
    result, df = translate(inp, 'csv\\test_0001_20221109122531.csv')
    # # 時刻形式を型一致させる
    m2 = re.search(r'\d{14}', 'test_0001_20221109122531.csv')
    t = m2.group()
    expected.insert(1, "time", datetime.datetime.strptime(t, "%Y%m%d%H%M%S"))
    expected['inputdate'] = expected["inputdate"].astype('datetime64')
    df['inputdate'] = df["inputdate"].astype('datetime64')
    print(expected)
    print(df)
    assert_frame_equal(df, expected, check_datetimelike_compat=True)
    assert result == True

def test_translate_filename_error():
    result, _ = translate('', '')
    assert result == False

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