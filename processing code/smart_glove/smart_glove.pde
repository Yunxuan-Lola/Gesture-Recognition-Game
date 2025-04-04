import processing.serial.*; // Import serial library
import java.net.*;
import java.io.*;

ServerSocket server;
Socket client;
BufferedReader reader;

//Serial myPort; // Serial object
//String portName;
//int gestureID = 10; // Stores the received gesture ID
String gesture = "none";

//declare images
PImage thumbup;
PImage scissors;
PImage paper;
PImage rock;

PImage game2;
PImage tiger;
PImage chicken;
PImage stick;


void setup() {
  size(800, 600, P3D); // Window size
  
  //portName = Serial.list()[6]; // Replace with your actual port
  //myPort = new Serial(this, portName, 115200);
  //myPort.bufferUntil('\n'); // Read until newline character
  try {
    server = new ServerSocket(6001);
    println("Waiting for python...");
    client = server.accept();
    println("Connected to Python..");
    reader = new BufferedReader(new InputStreamReader(client.getInputStream()));
  } catch (IOException e) {
    e.printStackTrace();
  }
  
  // Load images
  thumbup = loadImage("+1.png"); 
  scissors= loadImage("v.png");
  paper = loadImage("paper.png");
  rock = loadImage("rock.png");
  
  game2= loadImage("game2.png");
  tiger = loadImage("tiger.png");
  chicken = loadImage("chicken.png");
  stick = loadImage("stick.png");
}

void draw() {
  background(255); // White background
  requestData();
  // Display the detected gesture in canvas
  //println(gesture);
  displayGesture(gesture);

  //delay(300);
}

void requestData() {
  //Serial myPort = new Serial(this, portName, 115200); // Initialize serial communication
  //delay(500);
  //myPort.write('R');
  //String inString = myPort.readStringUntil('\n'); // Read incoming data
  String inString = null;
  try {
    if (reader.ready()) {
      inString = reader.readLine();
      //println("Received gesture:", gesture);
    }
  } catch (IOException e) {
    e.printStackTrace();
  }
  if (inString != null) {
    println("[Processing] Raw Received Data: " + inString); // Debug output
    inString = inString.trim(); // Remove spaces or newline characters
    gesture = inString;
    println("[Processing] Parsed Gesture ID: " + gesture);
    } else {
      println("!️ Invalid data received: " + inString); // Handle unexpected data
    }
    //try {
    //  gestureID = int(inString); // Convert to integer (1-8)
    //  //in console window
    //  println("Received Gesture ID: " + gestureID);
    //} catch (Exception e) {
    //  println("Invalid data: " + inString); // Handle unexpected data
    //}
  //myPort.stop(); 
}

//void serialEvent(Serial myPort) {

//}


//specify gesture instead of id
void displayGesture(String ges) {
  fill(0); 
  textSize(40);
  textAlign(CENTER, CENTER);

//basic display with text and bg color
  if(ges.equals("start1")) {
      background(255, 0, 0); // Red
      //text("👾1️⃣", width/2, height/2 - 30);
      //text("👍", width/2, height/2 + 30);
      image(thumbup, width/2 - thumbup.width/2, height/2 - thumbup.height/2);
  } else if(ges.equals("scissor")){
      background(0, 255, 0); // Green
      //text("Scissors", width/2, height/2);
      image(scissors, width/2 - thumbup.width/2, height/2 - thumbup.height/2);
  } else if(ges.equals("paper")){
      background(0, 0, 255); // Blue
      //text("Paper", width/2, height/2);
      image(paper, width/2 - thumbup.width/2, height/2 - thumbup.height/2);
  } else if(ges.equals("rock")){
      background(255, 255, 0); // Yellow
      //text("Rock", width/2, height/2);
      image(rock, width/2 - thumbup.width/2, height/2 - thumbup.height/2);
  } else if(ges.equals("start2")){
      background(255, 0, 255); // Pink
      //text("Game 2 starts: ", width/2, height/2);
      image(game2, width/2 - thumbup.width/2, height/2 - thumbup.height/2);
  } else if(ges.equals("tiger")){
      background(0, 255, 255); // Cyan
      //text("Tiger", width/2, height/2);
      image(tiger, width/2 - thumbup.width/2, height/2 - thumbup.height/2);
  } else if(ges.equals("chick")){
      background(150, 75, 0); // Brown
      //text("Chicken", width/2, height/2);
      image(chicken, width/2 - thumbup.width/2, height/2 - thumbup.height/2);
  } else if(ges.equals("stick")){
      background(128, 0, 128); // Purple
      //text("Stick", width/2, height/2);
      image(stick, width/2 - thumbup.width/2, height/2 - thumbup.height/2);
  } else {
      text("Waiting for gesture...", width/2, height/2);
  }
}
