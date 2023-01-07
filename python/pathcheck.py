import os
from typing import Tuple
import re

def is_targetpath(objkey: str) -> bool:
    HIERARCHY_LAYERS = 6
    hierach_array = objkey.split('/')
    if len(hierach_array) != HIERARCHY_LAYERS:
        return False
    
    CHECK_DIR = 'Test/Test-Raw'
    root_dir = '/'.join(hierach_array[:2])
    if root_dir != CHECK_DIR:
        return False

    basename = os.path.basename(objkey)
    print(basename)
    _, ext = basename.split('.', 1)
    if ext != "csv.gz":
        return False
    

    return True

def translated_path(objkey: str) -> Tuple[str, str, str]:
    HIERARCHY_LAYERS = 6
    # OSに依存しないセパレータ
    hierach_array = objkey.split('/')
    if len(hierach_array) != HIERARCHY_LAYERS:
        return '', '', ''

    root_name = 'Test'
    table_name = hierach_array[1]
    if f'{root_name}/{table_name}/' not in [f'{root_name}/test/', f'{root_name}/tamago/', f'{root_name}/hoge/']:
        return '', '', ''

    basename = os.path.basename(objkey)
    if table_name not in basename:
        return '', '', ''

    print(re.search(r'\d{8}', basename))
    if re.search(r'\d{8}', basename) is None:
        return '', '', ''
    
    # 拡張子が.csv.gzになるのでsplitextは使えない
    filename, _ = basename.split('.', 1)
    objpath = '/'.join(hierach_array[2:5])
    dest = f'{root_name}/{table_name}-Load/{objpath}/{filename}.parquet'
    moved = f'{root_name}/{table_name}-Moved/{objpath}/{filename}.csv.gz'
    error = f'{root_name}/{table_name}-Error/{objpath}/{filename}.csv.gz'

    return dest, moved, error

# def usecase():
#     ## dir.getAllobj(path)
#     target_paths = []
#     for target in target_paths:
#         if is_targetpath(target) is False:
#             break

#         dest, moved = translated_path(target)
#         ## 処理する
