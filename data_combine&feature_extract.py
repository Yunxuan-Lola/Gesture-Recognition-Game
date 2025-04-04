# Numpy is utilized to manipulate data containers
import numpy as np

# Matplotlib is used for visualizing the data with images
import matplotlib.pyplot as plt

# Sklearn is used to create classifiers
from sklearn import svm
import pandas as pd
import glob
import os

gesture = ["start1", "rock", "scissor", "paper", "start2", "stick", "tiger", "chick"]
combine = True
# The data is loaded into a "matrix" structure with two dimensions
# data1 = np.loadtxt("./saving_data/training_start1_object1.csv", delimiter=",")
# data2 = np.loadtxt("./saving_data/training_rock_object1.csv", delimiter=",")
# data3 = np.loadtxt("./saving_data/training_scissor_object1.csv", delimiter=",")
# data4 = np.loadtxt("./saving_data/training_paper_object1.csv", delimiter=",")
# data5 = np.loadtxt("./saving_data/training_start2_object1.csv", delimiter=",")
# data6 = np.loadtxt("./saving_data/training_stick_object1.csv", delimiter=",")
# data7 = np.loadtxt("./saving_data/training_lion_object1.csv", delimiter=",")
# data8 = np.loadtxt("./saving_data/training_chick_object1.csv", delimiter=",")

for i in range(8):
    if combine == True:
        # 要合并的文件夹路径
        folder_path = "./saving_data"
        gesture_prefix = "training_"+gesture[i]+"_object"  # 可以根据你的手势类别更换
        pattern = os.path.join(folder_path, f"{gesture_prefix}*.csv")

        # 找到所有匹配的文件
        file_list = glob.glob(pattern)
        print(f"Found {len(file_list)} files.")

        # 读取并合并所有文件
        df_list = []
        for file in file_list:
            df = pd.read_csv(file)
            # 如果文件里不含标题行（你可以删除 header=None）
            df_list.append(df)

        # 合并成一个大 DataFrame
        combined_df = pd.concat(df_list, ignore_index=True)

        # 输出信息
        print("Combined shape:", combined_df.shape)
        print("Preview:\n", combined_df.head())

        # 保存合并结果（可选）
        output_file = os.path.join(folder_path, "training_"+gesture[i]+"_combined.csv")
        combined_df.to_csv(output_file, index=False)
        print(f"Combined data saved to: {output_file}")



    # 读取合并数据
    df = pd.read_csv("./saving_data/training_"+gesture[i]+"_combined.csv")

    # 只保留数值列用于特征提取
    sensor_cols = ["Sensor4", "Sensor5", "Sensor8", "Sensor9"]
    label_col = "Label"

    # 滑动窗口参数
    window_size = 10  # 每个窗口包含50个时间点
    step_size = 5  # 每次滑动25个点（即50%重叠）


    # 保存提取后的特征数据
    features = []
    labels = []

    for start in range(0, len(df) - window_size + 1, step_size):
        end = start + window_size
        window = df.iloc[start:end]

        # 对每个传感器通道提取特征（mean, std, min, max）
        feature_vector = []
        for col in sensor_cols:
            data = window[col].astype(float)
            feature_vector.extend([
                data.mean(),
                data.std(),
                data.min(),
                data.max()
            ])

        # 获取窗口中多数 Label（假设是同一动作）
        label = window[label_col].mode()[0]

        features.append(feature_vector)
        labels.append(label)

    # 转为 NumPy array / DataFrame
    X = np.array(features)
    y = np.array(labels)

    print("X shape:", X.shape)  # (num_windows, 4 sensors × 4 features = 16)
    print("y shape:", y.shape)

    # 可选：保存提取结果
    feature_df = pd.DataFrame(X, columns=[
        f"{col}_{stat}"
        for col in sensor_cols
        for stat in ["mean", "std", "min", "max"]
    ])
    feature_df["Label"] = y
    feature_df.to_csv("./saving_data/features_"+gesture[i]+".csv", index=False)
    print("Feature:"+gesture[i]+ " file saved!")