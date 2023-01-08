import jaconv

def unificate_moji(moji: str) -> str:
    converted_2_han_moji = jaconv.zenkaku2hankaku(moji, kana=False, digit=True, ascii=True)
    converted_2_zen_moji = jaconv.hankaku2zenkaku(converted_2_han_moji, kana=True, digit=False, ascii=False)
    return converted_2_zen_moji
