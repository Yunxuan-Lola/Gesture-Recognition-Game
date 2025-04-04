import socket
import csv
import datetime
import joblib
import time

gesture_all = ["start1", "rock", "scissor", "paper", "start2", "stick", "tiger", "chick"]
# Server settings
HOST = "0.0.0.0"  # Listens on all available interfaces
PORT = 5001  # Must match Arduino's serverPort
# print(datetime.datetime.now())
# Create a socket (IPv4, TCP)
for i in range(len(gesture_all)):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # Allow reusing the same port
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Listening for connections on port {PORT}...")

    # Accept connection
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    print(f"[INFO] !!! now testing gesture: {gesture_all[i]}")
    # Open CSV file for writing data
    time.sleep(3)  # Preparation time between gestures
    csv_filename = "./saving_data/training_"+gesture_all[i]+"_object9.csv"
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Sensor4", "Sensor5", "Sensor8", "Sensor9", "Label"])  # Header

        start_time = time.time()
        try:
            while True:
                current_time = time.time()
                if current_time - start_time >= 10:
                    print(f"[INFO] Finished 10s recording for gesture: {gesture_all[i]}")
                    break

                data = client_socket.recv(1024).decode("utf-8").strip()

                # In case multiple data points come in one packet, split by semicolon
                packets = data.split(';')
                for packet in packets:
                    if packet.strip() == "":
                        continue  # skip empty strings

                    values = packet.strip().split(',')
                    if len(values) == 4:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        writer.writerow([timestamp] + values + [gesture_all[i]])  # Add label
                        file.flush()
                        print(f"Saved: {values}")
                    else:
                        print(f"Invalid packet: {packet}")


                # if data:
                #     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #     print(f"Received: {data}")
                #     data = data.split(',')[0]
                #     # Save to CSV
                #     writer.writerow([timestamp, data1, data2, data3, data4, "pressed"]) # add the label here
                #     file.flush()  # Ensure data is written immediately
        except KeyboardInterrupt:
            print("Server stopped.")
        finally:
            client_socket.close()
            server_socket.close()
            print(f"[INFO] Closed connection for gesture: {gesture_all[i]}")
            time.sleep(3)  # Pause before next gesture
