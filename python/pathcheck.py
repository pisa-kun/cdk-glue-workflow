import os

def is_targetpath(path: str) -> bool:
    _, ext = os.path.splitext(path)
    if ext != ".csv":
        return False
    
    HIERARCHY_LAYERS = 6
    # OSに依存しないセパレータ
    hierach_array = path.split(os.sep)
    if len(hierach_array) != HIERARCHY_LAYERS:
        return False

    CHECK_DIR = os.path.join('Test','Test-Raw')
    root_dir = os.path.join(hierach_array[0], hierach_array[1])
    if root_dir != CHECK_DIR:
        return False
    
    return True

def translated_path(path: str) -> (str, str):
    HIERARCHY_LAYERS = 6
    # OSに依存しないセパレータ
    hierach_array = path.split(os.sep)
    if len(hierach_array) != HIERARCHY_LAYERS:
        return '', ''

    DEST_DIR = os.path.join('Test','Test-Load')
    MOVED_DIR = os.path.join('Test','Test-Moved')

    dest = os.path.join(DEST_DIR, os.sep.join(hierach_array[2:]))
    moved = os.path.join(MOVED_DIR, os.sep.join(hierach_array[2:]))
    return dest, moved

# def usecase():
#     ## dir.getAllobj(path)
#     target_paths = []
#     for target in target_paths:
#         if is_targetpath(target) is False:
#             break

#         dest, moved = translated_path(target)
#         ## 処理する