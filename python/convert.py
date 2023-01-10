import jaconv
import re

def unificate_moji(moji: str) -> str:
    converted_2_han_moji = jaconv.zenkaku2hankaku(moji, kana=False, digit=True, ascii=True)
    converted_2_zen_moji = jaconv.hankaku2zenkaku(converted_2_han_moji, kana=True, digit=False, ascii=False)
    return converted_2_zen_moji

def is_target_serial(serial: str) -> bool:
    '''
    1文字目が数字、残りは英数字の合計10文字
    '''
    if (len(serial) == 10) is False:
        return False
    
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