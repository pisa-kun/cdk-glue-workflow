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

#### 文字チェック
シリアル情報の見切り、10or11文字、先頭2文字がアルファベット、残りが英数字、先頭2文字には特定文字は含まれない|