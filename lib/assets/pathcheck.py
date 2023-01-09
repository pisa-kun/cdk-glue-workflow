import os
from typing import Tuple
import re

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

    if re.search(r'\d{4}_\d{8}', basename) is None:
        return False

    _, ext = basename.split('.', 1)
    print(ext)
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

    if re.search(r'\d{4}_\d{8}', basename) is None:
        return False, None
    
    # 拡張子が.csv.gzになるのでsplitextは使えない
    filename, _ = basename.split('.', 1)
    objpath = '/'.join(hierach_array[2:5])
    dest = f'{root_name}/{table_name}_Load/{objpath}/{filename}.parquet'
    moved = f'{root_name}/{table_name}_Moved/{objpath}/{filename}.csv.gz'
    error = f'{root_name}/{table_name}_Error/{objpath}/{filename}.csv.gz'

    return True, TranslatedPaths(dest, moved, error)

# def usecase():
#     ## dir.getAllobj(path)
#     target_paths = []
#     for target in target_paths:
#         if is_targetpath(target) is False:
#             break

#         dest, moved = translated_path(target)
#         ## 処理する

