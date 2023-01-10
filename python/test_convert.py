import pytest

from convert import unificate_moji, is_target_model, is_target_serial

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

@pytest.mark.parametrize(('input_model', 'expected_result'), [
    ('CF12345abc', True), # CF始まりの10文字
    ('CF12345abcd', True), # CF始まりの11文字
    ('FZ12345ABC', True), # FZ始まりの10文字
    ('FZ12345ABCD', True), # FZ始まりの11文字
    ('CF12345abcde', False), # 10,11文字でない(>11)
    ('FZ12345AB', False), # 10,11文字でない(<10)
    ('pw12345ABC', False), # 先頭2文字がCF,FZでない
    ('cf12345ABC', False), # 先頭2文字がCF,FZでない/小文字
    ('XCF12345AB', False), # 先頭2文字がCF,FZでない/2,3文字目に含む
    ('CFtttt01aあ', False), # 英数字を含まないパターン
    ('cf-ttt01aa', False), # 記号を含むパターン
])
def test_is_target_model(input_model, expected_result):
    assert is_target_model(input_model) == expected_result

@pytest.mark.parametrize(('input_serial', 'expected_result'), [
    ('0000000000', True), # 10文字
    ('0H888aaaaa', True), # 
    ('00000000000', False), # 10文字でない(>10)
    ('000000000', False), # 10文字でない(<10)
    ('FZ12345ABC', False), # 1文字目が数字でない
    ('0H22-00000', False), # 英数字以外が2文字目以降に存在する
])
def test_is_target_serial(input_serial, expected_result):
    assert is_target_serial(input_serial) == expected_result