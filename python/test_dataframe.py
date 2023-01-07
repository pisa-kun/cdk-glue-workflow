import pandas as pd
from pandas.util.testing import assert_frame_equal

from dataframe import initialize, translate, init_dataframe

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

def test_init_dataframe():
    inp = init_dataframe("csv\\foo.test.csv.gz")
    exp = pd.DataFrame({
        'name': ['rinze', 'natsuha', 'cyoko'],
        'actor': ["maruoka", "akiho", "harusu"],
        'height': [178,173,169],
    })
    print(inp)
    print(exp)
    assert_frame_equal(inp, exp)