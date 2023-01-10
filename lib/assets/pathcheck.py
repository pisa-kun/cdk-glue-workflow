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

def is_target_serial(serial: str) -> bool:
    '''
    1文字目が数字、残りは英数字の合計10文字
    '''    
    if re.match('^\d[0-9a-zA-Z]{9}$', serial) is None:
        return False
    
    return True

def is_target_model(model: str) -> bool:
    '''
    10or11文字、先頭2文字がCF or FZ、残りが英数字
    '''
    if (len(model) == 10 or len(model) == 11) is False:
        return False

    if (model.startswith(('CF', 'FZ'))) is False:
        return False
    
    if re.match('^[a-zA-Z0-9]+$', model) is None:
        return False
    
    return True

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

# def usecase():
#     ## dir.getAllobj(path)
#     target_paths = []
#     for target in target_paths:
#         if is_targetpath(target) is False:
#             break

#         dest, moved = translated_path(target)
#         ## 処理する

