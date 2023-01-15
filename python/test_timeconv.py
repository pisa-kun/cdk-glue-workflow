import pytest
import datetime

from timeconv import convert_str2datetime_jst2utc

@pytest.mark.parametrize(('input_time_str', 'expected_yyyy','expected_MM','expected_dd',
'expected_hh','expected_mm', 'expected_ss'), [
    ('2012-12-29 13:49:37', 2012,12,29,4,49,37), #通常変換
    ('2012-12-29 05:49:37', 2012,12,28,20,49,37), #1日戻り
    ('2012-12-01 05:49:37', 2012,11,30,20,49,37), #1月戻り
    ('2013-01-01 05:49:37', 2012,12,31,20,49,37), #1年戻り
    ('20121229134937', 2012,12,29,4,49,37), #通常変換(連続文字)
    ('2012/12/29 13:49:37', 2012,12,29,4,49,37), #通常変換(/区切り)
])
def test_is_target_model(input_time_str, expected_yyyy, expected_MM, expected_dd, expected_hh, expected_mm, expected_ss):
    dtime = convert_str2datetime_jst2utc(input_time_str)
    assert dtime.year == expected_yyyy
    assert dtime.month == expected_MM
    assert dtime.day == expected_dd
    assert dtime.hour == expected_hh
    assert dtime.minute == expected_mm
    assert dtime.second == expected_ss

def test_convert_str2datetime_jst2utc_notformat():
    with pytest.raises(Exception) as e:
        _ = test_convert_str2datetime_jst2utc_notformat('2021 12 31 10:21:31')