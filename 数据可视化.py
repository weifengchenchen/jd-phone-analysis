import pandas as pd
import matplotlib.pyplot as plt

# 读取 LSTM 预测结果
output_lstm_filename = r"D:\Deskop\Code\Python_code\Data\lstm_predictions.csv"
lstm_df = pd.read_csv(output_lstm_filename)

# 绘制每个产品的预测结果
products = lstm_df['Product'].unique()

for product in products:
    product_df = lstm_df[lstm_df['Product'] == product]

    # 分离训练集和测试集
    train_df = product_df[product_df['Type'] == 'Train']
    test_df = product_df[product_df['Type'] == 'Test']

    plt.figure(figsize=(14, 7))

    # 绘制训练集的实际值和预测值
    plt.plot(train_df.index, train_df['Actual'], label='Actual (Train)', marker='o')
    plt.plot(train_df.index, train_df['Predicted'], label='Predicted (Train)', marker='x')

    # 绘制测试集的实际值和预测值
    plt.plot(test_df.index, test_df['Actual'], label='Actual (Test)', marker='o')
    plt.plot(test_df.index, test_df['Predicted'], label='Predicted (Test)', marker='x')

    plt.title(f'{product} LSTM Predictions')
    plt.xlabel('Sample Index')
    plt.ylabel('Rating')
    plt.legend()
    plt.grid(True)
    plt.show()



