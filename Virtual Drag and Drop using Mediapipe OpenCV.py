import cv2
import mediapipe as mp

# Initialize Mediapipe hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Rectangle properties for the letters "ZigGgy"
letters = ['i', 'g', 'Z', 'G', 'y', 'g']
num_rectangles = len(letters)
rectangle_width = 150  # Width of each rectangle
rectangle_height = 150  # Height of each rectangle
frame_width = 1280  # Width of the frame
frame_height = 720  # Height of the frame

# New string properties
text_string = "An AI Assistant"
text_rect_width = 500  # Width of the text rectangle
text_rect_height = 100  # Height of the text rectangle

# Calculate the total width of all rectangles and the space between them
total_rectangles_width = rectangle_width * num_rectangles
padding = (frame_width - total_rectangles_width) // 2  # Equal padding on both sides

# Recalculate the rectangle positions to have equal distance from the frame
rectangles = []
for i in range(num_rectangles):
    x1 = padding + i * rectangle_width
    y1 = 50
    x2 = x1 + rectangle_width
    y2 = y1 + rectangle_height
    rectangles.append((x1, y1, x2, y2))

# Add the movable text rectangle (for the string "An AI Assistant")
text_rectangle = [frame_width // 2 - text_rect_width // 2, 400, frame_width // 2 + text_rect_width // 2, 400 + text_rect_height]

# Dragging state variables for two hands and text box
dragging = [False, False]  # Dragging state for each hand
selected_rectangles = [-1, -1]  # Selected rectangle for each hand
offsets = [(0, 0), (0, 0)]  # Offsets for each hand
dragging_text = False  # Dragging state for the text box
selected_text = -1  # Selected text box
text_offset = (0, 0)  # Offset for the text box


def calculate_distance(pt1, pt2):
    """Calculate the Euclidean distance between two points."""
    return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame for a mirrored effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe Hands
    result = hands.process(rgb_frame)

    # Track up to two hands
    hand_positions = []  # Store index fingertip and thumb tip for both hands
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get the coordinates of the index fingertip and thumb tip
            h, w, _ = frame.shape
            index_finger_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            index_fingertip = (int(index_finger_landmark.x * w), int(index_finger_landmark.y * h))
            thumb_tip = (int(thumb_landmark.x * w), int(thumb_landmark.y * h))

            hand_positions.append((index_fingertip, thumb_tip))

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Handle rectangle movement logic for each hand
    for hand_idx, (index_fingertip, thumb_tip) in enumerate(hand_positions[:2]):
        # Calculate the distance between index fingertip and thumb tip
        pinch_distance = calculate_distance(index_fingertip, thumb_tip)
        ix, iy = index_fingertip

        if pinch_distance < 50:  # Adjust threshold for pinch detection
            if not dragging[hand_idx]:
                # Check if fingertip is inside any rectangle to select it
                for i, (x1, y1, x2, y2) in enumerate(rectangles):
                    if x1 <= ix <= x2 and y1 <= iy <= y2:
                        selected_rectangles[hand_idx] = i
                        offsets[hand_idx] = (ix - x1, iy - y1)
                        dragging[hand_idx] = True
                        break
                # Check if fingertip is inside the text box to select it
                if text_rectangle[0] <= ix <= text_rectangle[2] and text_rectangle[1] <= iy <= text_rectangle[3]:
                    selected_text = 0
                    text_offset = (ix - text_rectangle[0], iy - text_rectangle[1])
                    dragging_text = True
        else:
            # Release the rectangle or text when pinch is released
            dragging[hand_idx] = False
            selected_rectangles[hand_idx] = -1
            dragging_text = False
            selected_text = -1

        if dragging[hand_idx] and selected_rectangles[hand_idx] != -1:
            # Update rectangle position based on fingertip
            x1 = ix - offsets[hand_idx][0]
            y1 = iy - offsets[hand_idx][1]
            x2 = x1 + (rectangles[selected_rectangles[hand_idx]][2] - rectangles[selected_rectangles[hand_idx]][0])
            y2 = y1 + (rectangles[selected_rectangles[hand_idx]][3] - rectangles[selected_rectangles[hand_idx]][1])
            rectangles[selected_rectangles[hand_idx]] = (x1, y1, x2, y2)

        if dragging_text and selected_text != -1:
            # Update text position based on fingertip
            x1 = ix - text_offset[0]
            y1 = iy - text_offset[1]
            x2 = x1 + text_rect_width
            y2 = y1 + text_rect_height
            text_rectangle = [x1, y1, x2, y2]

    # Draw rectangles and letters
    for i, (x1, y1, x2, y2) in enumerate(rectangles):
        # Set color for the rectangles based on whether they are selected or not
        if i in selected_rectangles:
            color = (0, 255, 0)  # Selected rectangle color (green)
        else:
            color = (255, 0, 0)  # Non-selected rectangle color (blue)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)

        # Draw letter in the rectangle center with increased font size
        letter = letters[i]
        font_scale = 2  # Increase font size
        text_x = x1 + (x2 - x1) // 2 - 20
        text_y = y1 + (y2 - y1) // 2 + 20
        cv2.putText(frame, letter, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 3)

    # Draw the movable text rectangle and the string "An AI Assistant"
    if dragging_text:
        color = (0, 255, 0)  # Green when dragging
    else:
        color = (255, 255, 255)  # White when not dragging

    cv2.rectangle(frame, (text_rectangle[0], text_rectangle[1]), (text_rectangle[2], text_rectangle[3]), color, -1)

    # Calculate text size to center it within the box
    (text_width, text_height), baseline = cv2.getTextSize(text_string, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
    text_x = text_rectangle[0] + (text_rect_width - text_width) // 2
    text_y = text_rectangle[1] + (text_rect_height + text_height) // 2

    # Draw the centered text
    cv2.putText(frame, text_string, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

    # Show fingertip and thumb tip positions
    for index_fingertip, thumb_tip in hand_positions:
        cv2.circle(frame, index_fingertip, 10, (0, 255, 255), -1)
        cv2.circle(frame, thumb_tip, 10, (255, 255, 0), -1)

    # Display the frame
    cv2.imshow("Two-Handed Drag and Drop", frame)

    # Exit on ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
