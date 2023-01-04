import pandas as pd
from dataframe import initialize, translate

df = pd.DataFrame({
    'name': ['rinze', 'natsuha', 'juri', 'kaho', 'chiyoko'],
    'age': [16, 20, 17, 12, 17],
    'theme': ['blue', 'green', 'yellow', '' , 'pink'],
})

# def test_initialize():
#     assert df == initialize

# def test_translate():
#     assert df == translate(df)