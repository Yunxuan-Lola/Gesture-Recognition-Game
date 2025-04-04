// === Gesture Game Using Socket Communication ===

import java.net.*;
import java.io.*;
import processing.serial.*;

// Networking
ServerSocket server;
Socket client;
BufferedReader reader;

// Game state
String gesture = "none";
String finalGesture = "none";
String currentScreen = "start"; // start, select_game, game1, game2, result
String[] gestureBuffer = new String[5];
int gestureBufferIndex = 0;
boolean gameReady = false;        // if recognize start1/start2
String pendingGame = "none";      // start screen
boolean showStartGameButton = false; // if display "start game" button

// Timing
int countdown = 3;
int lastCountdownTime;
boolean countdownStarted = false;
String meGesture = "none";
String computerGesture = "none";
String result = "";

// Images
PImage thumbup, scissors, paper, rock, game2, tiger, chicken, stick;

void setup() {
  size(800, 600, P3D);
  textAlign(CENTER, CENTER);

  // Load gesture images
  thumbup = loadImage("+1.png"); 
  scissors= loadImage("v.png");
  paper = loadImage("paper.png");
  rock = loadImage("rock.png");
  game2 = loadImage("game2.png");
  tiger = loadImage("tiger.png");
  chicken = loadImage("chicken.png");
  stick = loadImage("stick.png");

  // Setup server socket
  try {
    server = new ServerSocket(6001);
    println("Waiting for python...");
    client = server.accept();
    println("Connected to Python");
    reader = new BufferedReader(new InputStreamReader(client.getInputStream()));
  } catch (IOException e) {
    e.printStackTrace();
  }
}

void draw() {
  background(255);

  switch(currentScreen) {
    case "start":
      drawStartScreen();
      break;
    case "select_game":
      drawGameSelect();
      break;
    case "game1":
    case "game2":
      drawCountdownAndPlay();
      break;
    case "result":
      drawResult();
      break;
  }

  readGesture();
}

void drawStartScreen() {
  textSize(40);
  fill(0);
  text("🎮 Welcome to Gesture Game!", width/2, height/2 - 40);
  textSize(24);
  text("Click anywhere to start", width/2, height/2 + 20);
}

void drawGameSelect() {
  textSize(32);
  fill(0);
  text("✌️ Please choose a game by gesture", width/2, 50);
  image(thumbup, width/4 - thumbup.width/2, height/2 - thumbup.height/2);
  text("Start Game 1", width/4, height/2 + 100);
  image(game2, 3*width/4 - game2.width/2, height/2 - game2.height/2);
  text("Start Game 2", 3*width/4, height/2 + 100);

  if (!gameReady && gestureBufferIndex >= gestureBuffer.length) {
    String mode = majorityGesture();
    if (mode.equals("start1") || mode.equals("start2")) {
      pendingGame = mode.equals("start1") ? "game1" : "game2";
      showStartGameButton = true;
      gameReady = true;
    }
  }

  if (showStartGameButton) {
    int buttonX = pendingGame.equals("game1") ? width/4 - 60 : 3*width/4 - 60;
    int buttonY = height/2 + 140;
    fill(50, 200, 100);
    //rect(width/2 - 100, height - 120, 200, 60, 15);
    rect(buttonX, buttonY, 120, 40, 10);
    fill(255);
    textSize(18);
    text("Start " + (pendingGame.equals("game1") ? "Game 1" : "Game 2"), buttonX + 60, buttonY + 20);
    //text("Start Game", width/2, height - 90);
  }
}
void resetBuffer() {
  for (int i = 0; i < gestureBuffer.length; i++) {
    gestureBuffer[i] = null;
  }
  gestureBufferIndex = 0;
}

void drawCountdownAndPlay() {
  fill(0);
  textSize(30);
  text(currentScreen.equals("game1") ? "🤖 Game 1 (Rock Paper Scissors)" : "🐯 Game 2 (Animal Gestures)", width/2, 50);

  if (!countdownStarted) {
    countdown = 3;
    lastCountdownTime = millis();
    countdownStarted = true;
  }

  if (countdown > 0) {
    if (millis() - lastCountdownTime >= 1500) {
      countdown--;
      lastCountdownTime = millis();
      
      if (countdown == 1) {
        resetBuffer();  // 在1时重置缓冲区
      }
    }
    textSize(60);
    text(countdown, width/2, height/2);
  } else if (meGesture.equals("none")) {
    // Read and fix gesture
    meGesture = majorityGesture();
    computerGesture = getRandomGesture(currentScreen);
    result = getResult(meGesture, computerGesture);
    currentScreen = "result";
  }
}

void drawResult() {
  background(230);
  textSize(32);
  fill(0);
  text(currentScreen.equals("game1") ? "Game 1 Result" : "Game 2 Result", width/2, 40);

  fill(50);
  text("Me", width/4, 100);
  text("Computer", 3*width/4, 100);

  showGestureImage(meGesture, width/4);
  showGestureImage(computerGesture, 3*width/4);

  fill(0);
  textSize(36);
  text("🏆 " + result, width/2, height - 80);
}

void showGestureImage(String ges, float x) {
  PImage img = getGestureImage(ges);
  if (img != null) {
    image(img, x - img.width/2, height/2 - img.height/2);
  } else {
    text(ges, x, height/2);
  }
}

PImage getGestureImage(String g) {
  switch(g) {
    case "start1": return thumbup;
    case "scissor": return scissors;
    case "paper": return paper;
    case "rock": return rock;
    case "start2": return game2;
    case "tiger": return tiger;
    case "chick": return chicken;
    case "stick": return stick;
  }
  return null;
}

String getRandomGesture(String game) {
  String[] options = game.equals("game1") ? new String[]{"rock", "paper", "scissor"} : new String[]{"tiger", "stick", "chick"};
  return options[int(random(options.length))];
}

String getResult(String me, String comp) {
  if (me.equals(comp)) return "Draw!";

  // Rock-paper-scissors logic
  if (currentScreen.equals("game1")) {
    if ((me.equals("rock") && comp.equals("scissor")) ||
        (me.equals("paper") && comp.equals("rock")) ||
        (me.equals("scissor") && comp.equals("paper"))) return "You Win!";
  } else {
    // Game 2 - arbitrary logic (customize if needed)
        if ((me.equals("tiger") && comp.equals("chick")) ||
        (me.equals("stick") && comp.equals("tiger")) ||
        (me.equals("chick") && comp.equals("stick"))) 
    return "You Win!";
  }
  return "You Lose!";
}

void readGesture() {
  try {
    if (reader.ready()) {
      String line = reader.readLine().trim();
      if (line != null && line.length() > 0) {
        gesture = line;
        gestureBuffer[gestureBufferIndex % gestureBuffer.length] = gesture;
        gestureBufferIndex++;
      }
    }
  } catch (IOException e) {
    e.printStackTrace();
  }
}

String majorityGesture() {
  HashMap<String, Integer> countMap = new HashMap<String, Integer>();
  for (String g : gestureBuffer) {
    if (g == null) continue;
    countMap.put(g, countMap.getOrDefault(g, 0) + 1);
  }
  String maxGesture = "none";
  int maxCount = 0;
  for (String key : countMap.keySet()) {
    if (countMap.get(key) > maxCount) {
      maxCount = countMap.get(key);
      maxGesture = key;
    }
  }
  return maxGesture;
}

void resetGame() {
  gestureBufferIndex = 0;
  meGesture = "none";
  computerGesture = "none";
  countdownStarted = false;
  for (int i = 0; i < gestureBuffer.length; i++) gestureBuffer[i] = null;
}

void mousePressed() {
  if (currentScreen.equals("start")) {
    currentScreen = "select_game";
  } else if (currentScreen.equals("result")) {
    currentScreen = "select_game";
    resetGame();
  } else if (currentScreen.equals("select_game") && showStartGameButton) {
    currentScreen = pendingGame;
    resetGame();
    showStartGameButton = false;
    gameReady = false;
  }
}
