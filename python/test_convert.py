import pytest

from convert import unificate_moji

HALF_ASCII = ('!"#$%&\'()*+,-./:;<=>?@[\\]^_`~',
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
              'abcdefghijklmnopqrstuvwxyz{|} ')
FULL_ASCII = ('！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀～',
              'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ',
              'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝　')

@pytest.mark.parametrize(('input_str', 'expected_str'), [
    ('１２３456ＡＢＣdef', '123456ABCdef'),
    ('ｾﾞﾝｶｸｶﾀｶﾅゼンカクジョウタイ' , 'ゼンカクカタカナゼンカクジョウタイ'),
    ('ﾐﾑﾒﾓｬﾔｭﾕｮﾖﾗﾘﾙﾚﾛﾜｦﾝｰヮヰヱヵヶｳﾞヽヾ･｢｣｡､','ミムメモャヤュユョヨラリルレロワヲンーヮヰヱヵヶヴヽヾ・「」。、'),
    (FULL_ASCII[0], HALF_ASCII[0]), # アスキー文字の変換確認1
    (FULL_ASCII[1], HALF_ASCII[1]), # アスキー文字の変換確認2
    (FULL_ASCII[2], HALF_ASCII[2]), # アスキー文字の変換確認3
    ('｢ﾀﾞﾁﾁﾞｯﾂﾂﾞﾃﾃﾞﾄﾄﾞァアィイゥウェエォオ６７８９012345ＡＢＣＤＥＦＧHIJKLMNOPQRSTUVWXYZ｣',
'「ダチヂッツヅテデトドァアィイゥウェエォオ6789012345ABCDEFGHIJKLMNOPQRSTUVWXYZ」'), #複合パターン
    ('''Line1ｻｻﾞｼｼﾞｽｽﾞｾｾﾞｿｿﾞﾀ
Line2
Line3''', 
'''Line1サザシジスズセゼソゾタ
Line2
Line3'''),#改行を含んでいるパターン
    ('abc\t012\nＡＢＣ','abc\t012\nABC'), #エスケープシーケンスを含んでいるパターン
    ('＼', '\\'),  # バックスラッシュの変換(mojimoji対策)
])
def test_unificate_moji(input_str, expected_str):
    assert unificate_moji(input_str) == expected_str

@pytest.mark.parametrize(('input_str', 'expected_str'), [
    ('￥≒≠', '￥≒≠'),
    ('¥≒≠', '¥≒≠'),
    ('｟ ｠ ￠ ￡ ￢ ￣ ￤ ￥ ￦ │ ← ↑ → ↓ ■ ○', '｟ ｠ ￠ ￡ ￢ ￣ ￤ ￥ ￦ │ ← ↑ → ↓ ■ ○')
])
def test_unificate_not_ascii_moji(input_str, expected_str):
    assert unificate_moji(input_str) == expected_str