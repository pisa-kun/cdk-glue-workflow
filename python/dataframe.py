import pandas as pd
from typing import Tuple
import re
import datetime
from convert import unificate_moji

def initialize() -> pd.DataFrame:
    df = pd.DataFrame({
        'name': ['rinze', 'natsuha', 'juri', 'kaho', 'chiyoko'],
        'age': [16, 20, 17, 12, 17],
        'theme': ['blue', 'green', 'yellow', None , 'pink'],
    })
    return df

def translate(df: pd.DataFrame, dataname: str) -> Tuple[bool, pd.DataFrame]:
    try:
        # searchできない場合はm.groupで例外発生
        m = re.search(r'\d{4}', dataname)
        f = m.group()

        m2 = re.search(r'\d{14}', dataname)
        t = m2.group()

        # フォーマットの追加
        # 先頭に追加
        df.insert(0, "format", f)
        # 日付の追加
        # 2行目に追加
        df.insert(1, "time", datetime.datetime.strptime(t, "%Y%m%d%H%M%S"))

        # CF, FZのみ抜き出し
        isModel = df['serial'].str.startswith(("CF", "FZ"))

        # - 削除
        df['serial'] = df[isModel]['serial'].apply(lambda serial: serial.replace('-', ''))

        # memoフィールドの英数字を全角から半角に
        df['memo'] = df[isModel]['memo'].apply(lambda str: unificate_moji(str))

        # JST to UTC
        jst2utc = datetime.timedelta(hours=-9)
        df['inputdate'] = df[isModel]['inputdate'].apply(lambda str: (datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f") + jst2utc))

        return True, df[isModel]
    except Exception:
        return False, None
#print(translate(initialize()))

def init_dataframe(data) -> pd.DataFrame:
    #df = pd.read_csv(data, encoding='utf-8')
    df = pd.read_csv(data)
    #df["height"] = df["height"].apply(lambda x: x * 2)
    return df


df = init_dataframe("csv\\test_0001_20221109122531.csv")
print(df)
result, translated = translate(df, 'test_0001_20221109122531.csv')
print(result, translated)