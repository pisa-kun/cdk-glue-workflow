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

> pytest --cov --cov-branch --cov-report=html