# Virtual-Drag-and-Drop-using-Mediapipe OpenCV


This project implements a hand gesture-based drag-and-drop system using **Mediapipe Open Source Framework**. The program tracks hand gestures (specifically pinch gestures) to allow users to move predefined rectangles and text boxes on the screen. The rectangles contain letters from the word "ZigGgy", and a movable text box displays the string "An AI Assistant".

## Prerequisites

Before running the project, ensure that you have the following dependencies installed:

- Python 3.x
- OpenCV (`opencv-python`)
- Mediapipe (`mediapipe`)

To install the required dependencies, run:

```bash
pip install opencv-python mediapipe
```

## Features

- **Hand Tracking**: Uses Mediapipe's Hand model to detect hand landmarks and track the position of the hands in real-time.
- **Pinch Gesture**: The system detects a pinch gesture (when the index finger and thumb are close) to trigger drag-and-drop functionality.
- **Interactive Rectangles**: There are predefined draggable rectangles labeled with the letters "ZigGgy". You can move these rectangles around by pinching and dragging them.
- **Movable Text Box**: A rectangle containing the text "An AI Assistant" can also be moved using the pinch gesture.
- **Live Video Feed**: The project uses the webcam feed for real-time interaction, with the system showing detected hand landmarks and rectangles.

## How It Works

1. **Hand Detection**: The program uses Mediapipe to detect hand landmarks in each frame of the webcam video.
2. **Pinch Gesture Detection**: When the user forms a pinch gesture (by bringing the index finger and thumb together), the system detects which object (rectangle or text box) the user is interacting with.
3. **Drag-and-Drop**: Once a pinch is detected, the user can move the selected object around the screen.
4. **Feedback**: The rectangles change color (green when selected, blue when not), and the letters inside the rectangles are displayed in the center of each rectangle.

## File Structure

```
.
├── hand_gesture_drag_and_drop.py           # Python script for hand gesture-based drag and drop
└── README.md                               # Project description
```

## Usage

1. Install the required dependencies.
2. Run the Python script:

```bash
python hand_gesture_drag_and_drop.py
```

3. The webcam window will open, and you should see draggable rectangles and a movable text box.
4. To move any rectangle or the text box, perform the pinch gesture with your hand in front of the webcam.
5. Press **Esc** to exit the program.

## Code Explanation

- **Mediapipe Hand Tracking**: We initialize `mp.solutions.hands` to detect hand landmarks and process the frame to extract hand positions.
- **Pinch Gesture Detection**: The program calculates the Euclidean distance between the index finger and the thumb tip to detect when a pinch gesture occurs. If the pinch distance is below a threshold, the drag-and-drop functionality is activated.
- **Rectangles and Text Box**: Predefined rectangles are displayed with letters inside them, and a movable text box contains the string "An AI Assistant". Both of these elements can be dragged using the pinch gesture.

