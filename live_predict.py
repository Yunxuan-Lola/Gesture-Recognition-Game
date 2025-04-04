import serial
import time
import joblib
import socket
import csv
import datetime
import numpy as np
from collections import deque

# 假设你的模型已经训练好并保存为 joblib 文件
from sklearn.ensemble import RandomForestClassifier
# open port

#ser = serial.Serial('COM12', 115200, timeout=1)
time.sleep(2)  # 给串口一点初始化时间
# 加载模型
model = joblib.load("./saving_data/my_model.joblib")

HOST = "0.0.0.0"  # Listens on all available interfaces
PORT = 5001  # Must match Arduino's serverPort
# print(datetime.datetime.now())
# Create a socket (IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # Allow reusing the same port
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Listening for connections on port {PORT}...")

# Accept connection
client_socket, client_address = server_socket.accept()
client_socket.settimeout(2.0)
print(f"Connected to {client_address}")

# Socket 设置：发送预测结果到 Processing
PROCESSING_IP = "127.0.0.1"
PROCESSING_PORT = 6001
processing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
processing_socket.connect((PROCESSING_IP, PROCESSING_PORT))
print("Connected to Processing socket.")

window_size = 10  # 滑动窗口大小
buffer = deque(maxlen=window_size)
prediction_interval = 0.5  # 秒
last_prediction_time = time.time()

try:
    while True:
        #data = client_socket.recv(1024).decode("utf-8").strip()
        try:
            data = client_socket.recv(1024).decode("utf-8").strip()
            print("[RECV]", repr(data))  # 调试输出
        except socket.timeout:
            continue
        packets = data.split(';')

        for packet in packets:
            if not packet.strip():
                continue

            values = packet.strip().split(',')
            if len(values) == 4:
                try:
                    values = list(map(float, values))
                    buffer.append(values)

                    # 当 buffer 满了之后开始预测
                    current_time = time.time()
                    if len(buffer) == window_size and (current_time - last_prediction_time >= prediction_interval):
                        window = np.array(buffer)

                        # 特征提取（均值、标准差、最小值、最大值）
                        features = []
                        for i in range(4):  # Sensor4, Sensor5, Sensor8, Sensor9
                            ch = window[:, i]
                            features.extend([ch.mean(), ch.std(), ch.min(), ch.max()])

                        X_input = np.array(features).reshape(1, -1)
                        pred = model.predict(X_input)[0]
                        #ser.write((str(pred) + "\n").encode())
                        print("Predicted:", pred)

                        processing_socket.sendall((str(pred) + "\n").encode())
                        last_prediction_time = current_time

                        # 可选：将结果发回 Arduino 或 Processing（如果需要）
                        # client_socket.sendall((str(pred) + "\n").encode())

                except Exception as e:
                    print(f"Data error: {values}, {e}")
            else:
                print("Invalid packet:", packet)

except KeyboardInterrupt:
    print("Server stopped.")
finally:
    client_socket.close()
    server_socket.close()
    processing_socket.close()