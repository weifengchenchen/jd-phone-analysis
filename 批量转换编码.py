import os
import glob
import locale


target_encoding = locale.getpreferredencoding(do_setlocale=True)

# 遍历当前目录所有CSV文件
for csv_file in glob.glob('C:\\Users\\16075\\Desktop\\分析报告\\数据\\*.csv'):
    try:
        # 读取UTF-8文件（自动处理BOM）
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        # 写入ANSI编码文件
        with open(csv_file, 'w', encoding=target_encoding, errors='replace') as f:
            f.write(content)

        print(f"转换成功: {csv_file}")
    except Exception as e:
        print(f"转换失败 {csv_file}: {str(e)}")