import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. High-Sensitivity MediaPipe Setup
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.3, # Highly sensitive to fast movements
    min_tracking_confidence=0.6,
)
detector = vision.HandLandmarker.create_from_options(options)

# 2. Initialize Webcam Capture
cap = cv2.VideoCapture(0)
print("Press 'q' to close the application.")

# Premium Laser Color Palette (BGR Format) matching the video
laser_colors = [
    (255, 0, 128),   # Pink/Purple
    (0, 140, 255),   # Orange
    (0, 230, 255),   # Yellow
    (0, 255, 128),   # Neon Green
    (255, 191, 0)    # Cyan Blue
]
fingertip_ids = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    # Mirror effect for natural tracking
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Convert format for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = detector.detect(mp_image)

    # 3. Check if TWO hands are visible
    if results.hand_landmarks and len(results.hand_landmarks) == 2:
        
        # CRITICAL FIX: Sort hands by their X coordinate (Left to Right)
        # This keeps lines locked perfectly even when you cross or twist your hands!
        sorted_hands = sorted(results.hand_landmarks, key=lambda hand: hand[0].x)
        left_hand = sorted_hands[0]
        right_hand = sorted_hands[1]

        # Draw the unyielding laser lines between matching fingers
        for i, tip_id in enumerate(fingertip_ids):
            # Get Left Hand coordinate
            pt1 = left_hand[tip_id]
            cx1, cy1 = int(pt1.x * w), int(pt1.y * h)

            # Get Right Hand coordinate
            pt2 = right_hand[tip_id]
            cx2, cy2 = int(pt2.x * w), int(pt2.y * h)

            # --- RENDER PERFECT RIGID LINES ---
            # Thick outer laser glow
            cv2.line(frame, (cx1, cy1), (cx2, cy2), laser_colors[i], 5, lineType=cv2.LINE_AA)
            # Solid white core center (creates the geometric solid beam look)
            cv2.line(frame, (cx1, cy1), (cx2, cy2), (255, 255, 255), 2, lineType=cv2.LINE_AA)

            # Vibrant endpoints on fingertips
            cv2.circle(frame, (cx1, cy1), 6, laser_colors[i], -1, lineType=cv2.LINE_AA)
            cv2.circle(frame, (cx1, cy1), 2, (255, 255, 255), -1, lineType=cv2.LINE_AA)
            cv2.circle(frame, (cx2, cy2), 6, laser_colors[i], -1, lineType=cv2.LINE_AA)
            cv2.circle(frame, (cx2, cy2), 2, (255, 255, 255), -1, lineType=cv2.LINE_AA)

        # Draw the subtle geometric wireframe mesh on the hands seen in your images
        for hand_landmarks in [left_hand, right_hand]:
            for connection in [
                (0,1), (1,2), (2,3), (3,4),        # Thumb
                (0,5), (5,6), (6,7), (7,8),        # Index
                (9,10), (10,11), (11,12),          # Middle
                (13,14), (14,15), (15,16),         # Ring
                (0,17), (17,18), (18,19), (19,20)  # Pinky
            ]:
                start = hand_landmarks[connection[0]]
                end = hand_landmarks[connection[1]]
                cv2.line(
                    frame, 
                    (int(start.x * w), int(start.y * h)), 
                    (int(end.x * w), int(end.y * h)), 
                    (200, 200, 200), 1, lineType=cv2.LINE_AA
                )

    # Fallback indicator if only 1 hand is on screen
    elif results.hand_landmarks:
        for hand_landmarks in results.hand_landmarks:
            for tip_id in fingertip_ids:
                pt = hand_landmarks[tip_id]
                cv2.circle(frame, (int(pt.x * w), int(pt.y * h)), 4, (160, 160, 160), -1, lineType=cv2.LINE_AA)

    # Display the final frame
    cv2.imshow("Rigid Interconnected Laser Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
detector.close()