from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import numpy as np
import os
import glob
import joblib

model = 1
# 设置路径和匹配规则
folder = "./saving_data"
pattern = os.path.join(folder, "features_*.csv")

# 加载所有特征文件
file_list = glob.glob(pattern)
print(f"Found {len(file_list)} feature files.")

# 合并所有文件为一个大 dataframe
df_list = [pd.read_csv(f) for f in file_list]
df_all = pd.concat(df_list, ignore_index=True)

# 分离 X 和 y
X = df_all.drop("Label", axis=1).values
y = df_all["Label"].values
print("Label distribution:")
print(df_all["Label"].value_counts())
print("Unique labels in y:", np.unique(y))
print("Label distribution:\n", pd.Series(y).value_counts())

print("X shape:", X.shape)
print("y shape:", y.shape)


## test for just one file
'''
gesture = "rock"
# 加载 CSV 文件
df = pd.read_csv("./saving_data/features_"+gesture+".csv")

# 分离特征和标签
X = df.drop("Label", axis=1).values   # 所有列除 Label 外为特征
y = df["Label"].values                # Label 列为目标分类

print("X shape:", X.shape)  # (num_samples, num_features)
print("y shape:", y.shape)  # (num_samples,)
'''

# 数据准备
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

if model == 1:
    ## randomForest !!!!
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

if model == 2:
    ## SVM !!!!
    from sklearn.svm import SVC
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline

    clf = make_pipeline(StandardScaler(), SVC(kernel='rbf', C=1.0))
    clf.fit(X_train, y_train)

if model == 3:
    ## logistic regression !!!!
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    clf = make_pipeline(StandardScaler(), LogisticRegression(multi_class='multinomial', max_iter=1000))
    clf.fit(X_train, y_train)

joblib.dump(clf, "./saving_data/my_model.joblib")
# 预测与评估
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

