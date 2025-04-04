import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
import joblib
import glob
import os

# 你要评估的测试对象
test_objects = ["object7", "object8", "object9"]
gesture_all = ["start1", "rock", "scissor", "paper", "start2", "stick", "tiger", "chick"]
sensor_cols = ["Sensor4", "Sensor5", "Sensor8", "Sensor9"]
label_col = "Label"
window_size = 10
step_size = 5

# 载入模型
model = joblib.load("./saving_data/my_model.joblib")

# 合并原始测试数据
test_df_list = []
for gesture in gesture_all:
    for obj in test_objects:
        filepath = f"./saving_data/training_{gesture}_{obj}.csv"
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            test_df_list.append(df)

# 合并所有测试数据
test_data = pd.concat(test_df_list, ignore_index=True)

# 特征提取
features = []
labels = []

for start in range(0, len(test_data) - window_size + 1, step_size):
    end = start + window_size
    window = test_data.iloc[start:end]
    feature_vector = []
    for col in sensor_cols:
        data = window[col].astype(float)
        feature_vector.extend([data.mean(), data.std(), data.min(), data.max()])
    label = window[label_col].mode()[0]
    features.append(feature_vector)
    labels.append(label)

# 转为 DataFrame
X_test = np.array(features)
y_test = np.array(labels)

# 预测与评估
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(X_test.shape, y_test.shape)
print(acc, report)