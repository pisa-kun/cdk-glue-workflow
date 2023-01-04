import pandas as pd
from pandas.util.testing import assert_frame_equal

from dataframe import initialize, translate

df = pd.DataFrame({
    'name': ['rinze', 'natsuha', 'juri', 'kaho', 'chiyoko'],
    'age': [16, 20, 17, 12, 17],
    'theme': ['blue', 'green', 'yellow', None , 'pink'],
})

def test_initialize():
    assert_frame_equal(initialize(), df)

def test_translate():
    expected = pd.DataFrame({
    'name': ['RINZE', 'NATSUHA', 'JURI', 'KAHO', 'CHIYOKO'],
    'age': [16, 20, 17, 12, 17],
    'theme': ['BLUE', 'GREEN', 'YELLOW', '' , 'PINK'],
    })
    assert_frame_equal(translate(df), expected)