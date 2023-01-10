import pandas as pd
import re
import datetime
from convert import unificate_moji, is_target_serial, is_target_model

# def initialize() -> pd.DataFrame:
#     df = pd.DataFrame({
#         'name': ['rinze', 'natsuha', 'juri', 'kaho', 'chiyoko'],
#         'age': [16, 20, 17, 12, 17],
#         'theme': ['blue', 'green', 'yellow', None , 'pink'],
#     })
#     return df

def translate(df: pd.DataFrame, dataname: str) -> pd.DataFrame:
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

    return df[isModel]

def translate2(df: pd.DataFrame, dataname: str) -> pd.DataFrame:
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

    df['model'] = df["model"].apply(lambda model: model.replace("-", ""))
    # FLAG=0 または ModelとSerialが条件を満たす
    isFlag = df["flag"] == 0
    isSerial = df["serial"].apply(lambda serial: is_target_serial(serial))
    isModel = df["model"].apply(lambda model: is_target_model(model))
    isTarget = isFlag | (isSerial & isModel)

    # 文字列型の英数字を全角から半角に
    varchar_headers = ['data1', 'data2']
    for varchar in varchar_headers:
        df[varchar] = df[varchar].apply(lambda str: unificate_moji(str))
        #df[varchar] = df[varchar].apply(lambda str: str if isinstance(str, int) or isinstance(str, float) else unificate_moji(str))
    
    # JST to UTC
    #jst2utc = datetime.timedelta(hours=-9)
    #df['time'] = df['time'].apply(lambda str: (datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S") + jst2utc))

    return df[isTarget]

def init_dataframe(data) -> pd.DataFrame:
    # na_filter=Trueの場合、空白文字がNaNになってしまう
    df = pd.read_csv(data, na_filter=False)
    return df


# df = init_dataframe("csv\\test_0001_20221109122531.csv")
# print(df)
# df.to_csv('csv\\test_0001_20221109122531.csv.gz', index=False, compression='gzip', encoding='utf-8')
# result, translated = translate(df, 'test_0001_20221109122531.csv')
# print(result, translated)

df = init_dataframe('csv\\hoge_0001_20230111122531.csv')
print(df)
df2 = translate2(df, 'hoge_0001_20230111122531.csv')
print(df2)
# # 全て""囲み
#df2.to_csv("csv\\hoge_0001_20230111122531.csv.gz", compression='gzip', index=False, quoting=1)