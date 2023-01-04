import pandas as pd

def initialize() -> pd.DataFrame:
    df = pd.DataFrame({
        'name': ['rinze', 'natsuha', 'juri', 'kaho', 'chiyoko'],
        'age': [16, 20, 17, 12, 17],
        'theme': ['blue', 'green', 'yellow', None , 'pink'],
    })
    return df

def translate(df: pd.DataFrame) -> pd.DataFrame:
    df["name"] = df["name"].apply(lambda name: name.upper())
    ## Noneの場合はupper()が使えないので、Noneを空白文字に処理する関数を用意する 
    # pythonの3項演算子 (lambda x: 'odd' if x % 2 else 'even')       
    df["theme"] = df["theme"].apply(lambda name: '' if name is None else name.upper())
    #df["theme"] = df["theme"].apply(lambda name: name.upper())
    return df

# df = translate()
# df["name"] = df["name"].apply(lambda name: name.upper())
# print(df)
print(translate(initialize()))