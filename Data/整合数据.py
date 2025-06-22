import pandas as pd
import glob
import os

# 获取所有CSV文件的路径
file_paths = glob.glob('D:\\Deskop\\Code\\Python_code\\Data\\*.csv')  # 替换为你的文件夹路径

# 初始化一个空列表来存储数据
data_list = []

# 定义可能的编码格式
encodings = ['utf-8', 'Ansi', 'utf-16']

# 遍历每个文件路径
for file_path in file_paths:
    for encoding in encodings:
        try:
            # 尝试读取CSV文件
            data = pd.read_csv(file_path, encoding=encoding)
            data_list.append(data)  # 将数据添加到列表中
            print(f"成功读取文件: {file_path}，编码: {encoding}")
            break  # 成功读取后跳出编码尝试循环
        except Exception as e:
            print(f"尝试读取文件 {file_path} 时失败，编码: {encoding}，错误: {e}")

# 合并所有数据
if data_list:
    combined_data = pd.concat(data_list, ignore_index=True)

    # 保存合并后的数据到新的CSV文件
    combined_data.to_csv('D:\\Deskop\\Code\\Python_code\\Data\\combined_data.csv', index=False, encoding='utf-8')
    print("所有CSV文件的数据已成功整合并保存为 combined_data.csv。")
else:
    print("没有成功读取任何文件。")