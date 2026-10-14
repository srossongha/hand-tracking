#!/usr/bin/env python3
import cv2
import mediapipe as mp
import numpy as np

# Hand skeleton connections (bone lines)
CONNECTIONS = [(c.start, c.end) for c in mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS]

# MediaPipe HandLandmarker setup
options = mp.tasks.vision.HandLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path="models/hand_landmarker.task"),
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    num_hands=2,
)
landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
frame_idx = 0

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    # Detect hands
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect_for_video(mp_img, frame_idx * 33)
    frame_idx += 1
    hands = result.hand_landmarks or []

    # When 2 hands are detected: connect thumb (4) and index (8) to create the box
    if len(hands) == 2:
        # Sort hands left to right by wrist x
        h_left, h_right = (hands[0], hands[1]) if hands[0][0].x <= hands[1][0].x else (hands[1], hands[0])

        box = np.array([
            [int(h_left[4].x * w), int(h_left[4].y * h)],    # Left thumb
            [int(h_left[8].x * w), int(h_left[8].y * h)],    # Left index
            [int(h_right[8].x * w), int(h_right[8].y * h)],  # Right index
            [int(h_right[4].x * w), int(h_right[4].y * h)],  # Right thumb
        ], dtype=np.int32)

        # Glitch filter: shift blue and red channels sideways
        b, g, r = cv2.split(frame)
        glitch = cv2.merge([np.roll(b, -12, axis=1), g, np.roll(r, 12, axis=1)])

        # Apply glitch ONLY inside the box
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(mask, [box], 255)
        frame[mask == 255] = glitch[mask == 255]

        # Draw box outline
        cv2.polylines(frame, [box], isClosed=True, color=(0, 255, 255), thickness=2, lineType=cv2.LINE_AA)

    # Draw the hand skeleton bone lines and joints on all detected hands
    for hand in hands:
        pts = [(int(lm.x * w), int(lm.y * h)) for lm in hand]
        for a, b in CONNECTIONS:
            cv2.line(frame, pts[a], pts[b], (0, 255, 0), 2, cv2.LINE_AA)
        for pt in pts:
            cv2.circle(frame, pt, 3, (0, 0, 255), -1, cv2.LINE_AA)

    cv2.imshow("Hand Box Glitch", frame)
    if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
        break

cap.release()
cv2.destroyAllWindows()