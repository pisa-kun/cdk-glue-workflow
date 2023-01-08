import jaconv
import re

def unificate_moji(moji: str) -> str:
    converted_2_han_moji = jaconv.zenkaku2hankaku(moji, kana=False, digit=True, ascii=True)
    converted_2_zen_moji = jaconv.hankaku2zenkaku(converted_2_han_moji, kana=True, digit=False, ascii=False)
    return converted_2_zen_moji

def is_target_number(number: str) -> bool:
    '''
    シリアル情報の見切り、10or11文字、先頭2文字がアルファベット、残りが英数字、
    先頭2文字には特定文字(I,O)は含まれない|
    '''
    if (len(number) == 10 or len(number) == 11) is False:
        return False
    
    pre2 = number[0:2]
    result = re.match('[a-zA-Z]', pre2)
    if result is None:
        return False
    
    result2 = re.match('[ioIO]', pre2)
    if result2:
        return False

    result3 = re.match('^[a-zA-Z0-9]+$', number)
    if result3 is None:
        return False

    return True