import pandas as pd
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

# 定义基础路径
base_path = r"D:\Deskop\Code\Python_code\Data"

# 定义产品列表
products = ["RedmiK80", "一加 Ace 5", "vivo iQOO Neo10"]

# 创建一个字典来存储每个产品的数据
data_dict = {}

# 读取每个产品的CSV文件
for product in products:
    csv_filename = os.path.join(base_path, product + ".csv")
    if os.path.exists(csv_filename):
        try:
            df = pd.read_csv(csv_filename, encoding='gbk')  # 尝试使用 gbk 编码
        except UnicodeDecodeError:
            print(f"Failed to read {csv_filename} with gbk encoding. Trying latin1...")
            try:
                df = pd.read_csv(csv_filename, encoding='latin1')  # 尝试使用 latin1 编码
            except UnicodeDecodeError:
                print(f"Failed to read {csv_filename} with latin1 encoding.")
                continue

        # 打印CSV文件的前几行，以便检查列名
        print(f"\nFirst few rows of {product}.csv:")
        print(df.head())

        # 检查是否有 '评分' 列
        if '评分' not in df.columns:
            print(f"'评分' column not found in {product}.csv. Available columns: {df.columns}")
            continue

        data_dict[product] = df['评分'].values.reshape(-1, 1)
    else:
        print(f"File not found: {csv_filename}")

# 数据标准化
scaler = StandardScaler()
scaled_data = {}
for product, ratings in data_dict.items():
    scaled_data[product] = scaler.fit_transform(ratings)

# 聚类分析
clusters = {}
cluster_list = []

for product, ratings in scaled_data.items():
    n_samples = len(ratings)
    if n_samples < 3:
        print(f"Not enough samples for clustering in {product}. Skipping clustering.")
        clusters[product] = None
        continue

    # 根据样本数量调整聚类数量
    n_clusters = min(3, n_samples)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(ratings).flatten()
    clusters[product] = cluster_labels

    # 添加到聚类结果列表
    for c in cluster_labels:
        cluster_list.append({'Product': product, 'Cluster': c})

cluster_df = pd.DataFrame(cluster_list)

# 保存聚类结果到新的CSV文件
output_cluster_filename = os.path.join(base_path, "clustering_results.csv")
cluster_df.to_csv(output_cluster_filename, index=False)
print(f"Clustering results saved to: {output_cluster_filename}")


# LSTM 预测
def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        a = data[i:(i + time_step), 0]
        X.append(a)
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)


time_step = 10
lstm_predictions = {}

for product, ratings in scaled_data.items():
    if len(ratings) <= time_step:
        print(f"Not enough samples for LSTM prediction in {product}. Skipping LSTM prediction.")
        lstm_predictions[product] = None
        continue

    X, y = create_dataset(ratings, time_step)

    # Reshape input to be [samples, time steps, features] which is required for LSTM
    X = X.reshape(X.shape[0], X.shape[1], 1)

    # Split into train and test sets
    train_size = int(len(X) * 0.8)
    test_size = len(X) - train_size
    X_train, X_test = X[0:train_size], X[train_size:len(X)]
    y_train, y_test = y[0:train_size], y[train_size:len(y)]

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer=Adam())

    # Train the model
    model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=2)

    # Make predictions
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    # Inverse transform the predictions
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    y_train = scaler.inverse_transform([y_train]).reshape(-1, 1)
    y_test = scaler.inverse_transform([y_test]).reshape(-1, 1)

    lstm_predictions[product] = {
        'train_predict': train_predict,
        'test_predict': test_predict,
        'y_train': y_train,
        'y_test': y_test
    }

# 打印LSTM预测结果
for product, prediction in lstm_predictions.items():
    if prediction is not None:
        print(f"{product} LSTM Predictions:")
        print(f"Train Predict: {prediction['train_predict']}")
        print(f"Test Predict: {prediction['test_predict']}")

# 保存LSTM预测结果到新的CSV文件
lstm_results = []
for product, prediction in lstm_predictions.items():
    if prediction is not None:
        for i in range(len(prediction['train_predict'])):
            lstm_results.append({
                'Product': product,
                'Type': 'Train',
                'Actual': prediction['y_train'][i][0],
                'Predicted': prediction['train_predict'][i][0]
            })
        for i in range(len(prediction['test_predict'])):
            lstm_results.append({
                'Product': product,
                'Type': 'Test',
                'Actual': prediction['y_test'][i][0],
                'Predicted': prediction['test_predict'][i][0]
            })

lstm_df = pd.DataFrame(lstm_results)
output_lstm_filename = os.path.join(base_path, "lstm_predictions.csv")
lstm_df.to_csv(output_lstm_filename, index=False)
print(f"LSTM predictions saved to: {output_lstm_filename}")