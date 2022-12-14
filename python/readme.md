### execution pytest

> pytest

> pip install pytest-cov

#### C0(命令網羅/ステートメント)確認
> pytest --cov

#### C1(分岐網羅/ブランチ)確認
> pytest --cov --cov-branch

```pythonshell
----------- coverage: platform win32, python 3.8.1-final-0 -----------
Name                Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------
pathcheck.py            4      0      0      0   100%
prime.py               13      1     10      1    91%
test_pathcheck.py       8      0      0      0   100%
test_prime.py           5      0      0      0   100%
-----------------------------------------------------
TOTAL                  30      1     10      1    95%
```

- Branchは条件分岐の数、BrPartは通っていない条件の数

#### separatorに注意
単体テスト環境がwindowsローカルの場合は**バックスラッシュ**でテスト、本番環境はLinux系なので**スラッシュ**になる

```py
    # OSに依存しないセパレータ
    hierach_array = path.split(os.sep)
```

文字列リストの連結

```py
list1 = ['yyyy', 'MM', 'dd', 'hoge-yyyyMMdd.csv']

result = os.sep.join(list1)
print(result)
# yyyy/MM/dd/hoge-yyyyMMdd.csv]
```

#### pandasのテスト

https://nwpct1.hatenablog.com/entry/pandas-testing

- Usage
```python
import pandas as pd
from pandas.util.testing import assert_frame_equal
from dataframe import initialize, translate

df = pd.DataFrame({
    'name': ['rinze', 'natsuha', 'juri', 'kaho', 'chiyoko'],
    'age': [16, 20, 17, 12, 17],
    'theme': ['blue', 'green', 'yellow', None , 'pink'],
})

def test_initialize():
    # assert_frame_equal(actual_df, expected_df)
   assert_frame_equal(initialize(), df)
```

#### pytest レポート出力

> pytest --cov --cov-branch --cov-report=html --cov-report=term-missing


#### 半角・全角処理

|  文字列  | 変換 | 例 |
| ---- | ---- | ---- |
|  英数字  |  半角に統一  | １２３456ＡＢＣdef → 123456ABCdef |
|  カタカナ  |  全角カタカナに統一  | ｾﾞﾝｶｸｶﾀｶﾅゼンカクジョウタイ → ゼンカクカタカナゼンカクジョウタイ|
|  Ascii文字  |  変換無し  | - |
|  全体複合  |  変換無し  | １２３456ＡＢＣdefｾﾞﾝｶｸｶﾀｶﾅゼンカク- ー/・!！ → 123456ABCdefゼンカクカタカナゼンカク- ー/・!！|


#### print/loggingの出力場所

- /aws-glue/python-jobs/output
- /aws-glue/python-jobs/error

printの場合はouput、loggingはerrorにデフォルト出力

https://yomon.hatenablog.com/entry/2019/07/gluepythonshelllog

#### dfの日付情報をＵＴするとき
```py
    expected = pd.DataFrame({
        'format': ['0001', '0001'],
        'serial': ['CFAA123', 'FZAA123'],
        'inputdate': ["2022-11-08 17:54:30", "2022-11-08 17:54:30"],
        'memo': ["0123456790ABCDefパイソン", "xyz789パイソンパイソン"],
    })
'''
```
E   DataFrame.iloc[:, 3] (column name="inputdate") values are different (100.0 %)
E   [index]: [0, 1]
E   [left]:  <DatetimeArray>
E   ['2022-11-08 17:54:30', '2022-12-08 17:54:30']
E   Length: 2, dtype: datetime64[ns]
E   [right]: [2022-11-08 17:54:30, 2022-11-08 17:54:30]
```

- astypeで datetime型にした後、check_datetimelike_compat=Trueにする
```python
    expected['inputdate'] = expected["inputdate"].astype('datetime64')
    df['inputdate'] = df["inputdate"].astype('datetime64')
    print(expected)
    print(df)
    assert_frame_equal(df, expected, check_datetimelike_compat=True)
```

#### gzip圧縮されたs3上のcsv読み込み
https://dev.classmethod.jp/articles/20200501-pandas-gzip-s3/

```python
    s3obj = s3.Object(TARGET_BUCKET, obj.key)
    body_in = gzip.decompress(s3obj.get()['Body'].read()).decode('utf-8')
    buffer_in = io.StringIO(body_in)
```

#### NaN対策

pandasはdataframe読み込み時に空白文字をNaNにしてしまう。文字列データに対して、処理を実施する場合に型が異なるエラーが発生するので空白文字にしたい

https://megatenpa.com/python/pandas/pandas-blank-nan/

df = pd.read_csv(data, na_filter=False)

#### 複合条件を満たすか

```python
        df['model'] = df["model"].apply(lambda model: model.replace("-", ""))
        # FLAG=0 または ModelとSerialが条件を満たす
        isFlag = df["flag"] == 0
        isSerial = df["serial"].apply(lambda serial: is_target_serial(serial))
        isModel = df["model"].apply(lambda model: is_target_model(model))
        isTarget = isFlag | (isSerial & isModel)
```

Flagチェックが不要な場合は、isSerial & isModelでOK