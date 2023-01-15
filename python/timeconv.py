import datetime
import re

def convert_str2datetime_jst2utc(tstr: str) -> datetime:
    dt = None
    # 正規表現で対象の文字列かチェック
    if(re.fullmatch(r'\d{14}', tstr)):
        dt = datetime.datetime.strptime(tstr, '%Y%m%d%H%M%S')
    elif(re.fullmatch('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', tstr)):
        dt = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
    elif(re.fullmatch('\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}', tstr)):
        dt = datetime.datetime.strptime(tstr, '%Y/%m/%d %H:%M:%S')
    else:
        raise

    # JST 2 UTC変換処理
    jst2utc = datetime.timedelta(hours=-9)
    return dt + jst2utc

