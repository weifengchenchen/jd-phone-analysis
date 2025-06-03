import pandas as pd

def drop(csv_filename):
    df = pd.read_csv(csv_filename, encoding='ansi')
    df=df.dropna(how='all')
    df.to_csv(csv_filename, index=False, encoding='ansi')
    print("清洗完成")