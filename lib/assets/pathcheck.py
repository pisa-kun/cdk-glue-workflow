import os
from typing import Tuple
import re
import pandas as pd
from typing import Tuple
import datetime
import jaconv

def unificate_moji(moji: str) -> str:
    converted_2_han_moji = jaconv.zenkaku2hankaku(moji, kana=False, digit=True, ascii=True)
    converted_2_zen_moji = jaconv.hankaku2zenkaku(converted_2_han_moji, kana=True, digit=False, ascii=False)
    return converted_2_zen_moji

def is_targetpath(objkey: str) -> bool:
    HIERARCHY_LAYERS = 6
    # OSに依存しないセパレータ
    hierach_array = objkey.split('/')
    if len(hierach_array) != HIERARCHY_LAYERS:
        return False

    root_name = 'Test'
    table_name = hierach_array[1]
    if f'{root_name}/{table_name}/' not in [f'{root_name}/test/', f'{root_name}/tamago/', f'{root_name}/hoge/']:
        return False

    basename = os.path.basename(objkey)
    if table_name not in basename:
        return False

    if re.search(r'\d{4}_\d{14}', basename) is None:
        return False

    _, ext = basename.split('.', 1)
    if ext != "csv.gz":
        return False

    return True

class TranslatedPaths:
    def __init__(self, dest: str, moved: str, error: str):
        self.dest = dest
        self.moved = moved
        self.error = error

def translated_path(objkey: str) -> Tuple[bool, TranslatedPaths]:
    HIERARCHY_LAYERS = 6
    # OSに依存しないセパレータ
    hierach_array = objkey.split('/')
    if len(hierach_array) != HIERARCHY_LAYERS:
        return False, None

    root_name = 'Test'
    table_name = hierach_array[1]
    if f'{root_name}/{table_name}/' not in [f'{root_name}/test/', f'{root_name}/tamago/', f'{root_name}/hoge/']:
        return False, None

    basename = os.path.basename(objkey)
    if table_name not in basename:
        return False, None

    if re.search(r'\d{4}_\d{14}', basename) is None:
        return False, None
    
    # 拡張子が.csv.gzになるのでsplitextは使えない
    filename, _ = basename.split('.', 1)
    objpath = '/'.join(hierach_array[2:5])
    dest = f'{root_name}/{table_name}_Load/{objpath}/{filename}.parquet'
    moved = f'{root_name}/{table_name}_Moved/{objpath}/{filename}.csv.gz'
    error = f'{root_name}/{table_name}_Error/{objpath}/{filename}.csv.gz'

    return True, TranslatedPaths(dest, moved, error)

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

def init_dataframe(data) -> pd.DataFrame:
    ## TODO:読み込みエラーの理由
    df = pd.read_csv(data)
    # df = pd.read_csv(data, compression='gzip', encoding='utf-8', sep='\t')
    return df

# def usecase():
#     ## dir.getAllobj(path)
#     target_paths = []
#     for target in target_paths:
#         if is_targetpath(target) is False:
#             break

#         dest, moved = translated_path(target)
#         ## 処理する

