import chardet
import pandas as pd


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']
def drop(csv_filename):
    # 1. 检测原始编码（可能是 utf-8、gbk 等）
    original_encoding = detect_encoding(csv_filename)
    # 2. 读取 CSV（使用检测到的编码）
    df = pd.read_csv(csv_filename, encoding=original_encoding)
    # 3. 删除全空行（可选）
    df = df.dropna(how='all')

    # 4. 保存为 ANSI（gbk）
    df.to_csv(csv_filename, index=False, encoding='Ansi',errors='ignore')
    print(f"转换完成: {csv_filename}")