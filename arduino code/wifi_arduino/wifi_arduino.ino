#include <SPI.h>
#include <WiFiNINA.h>

// WiFi credentials
const char* ssid = "error";     // Replace with your WiFi SSID
const char* password = "zhuzhuzhu"; // Replace with your WiFi password

// Server details (your computer's IP and port)
const char* serverIP = "192.168.91.220";  // Replace with your computer's local IP/ the IP after your computer connect to the hotspot
const int serverPort = 5001;  // Must match the server Python script

//int sensorPin1 = A1;
//int sensorValue1 = 0;
//const int buttonPin = 2;
int sensorPin4 = A2;
int sensorPin5 = A1;
int sensorPin8 = A4;
int sensorPin9 = A3;

int sensor4 = 0;
int sensor5 = 0;
int sensor8 = 0;
int sensor9 = 0;

WiFiClient client;

void setup() {
    Serial.begin(115200);
    while (!Serial);

    // Connect to WiFi
    Serial.print("Connecting to WiFi...");
    while (WiFi.begin(ssid, password) != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println("Connected!");

    // Connect to the server
    Serial.print("Connecting to server...");
    while (!client.connect(serverIP, serverPort)) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println("Connected to server!");
}

void loop() {
    if (client.connected()) {
        sensor4 = analogRead(sensorPin4);  // Read from a sensor (adjust as needed)
        sensor5 = analogRead(sensorPin5);
        sensor8 = analogRead(sensorPin8);
        sensor9 = analogRead(sensorPin9);
        // int test_value = digitalRead(buttonPin);
        String data = String(sensor4) + "," + String(sensor5) + "," + String(sensor8) + "," + String(sensor9) + ";" ;  // Convert to string，typo in previous version code
        client.print(data);  // Send data
        //Serial.print("Sent: ");
        //Serial.println(data);
        delay(100);  // Adjust sending rate/frequency
    } else {
        //Serial.println("Disconnected, reconnecting...");
        client.stop();
        delay(2000);
        client.connect(serverIP, serverPort);
    }
}
