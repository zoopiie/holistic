import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    max_num_hands=2,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style())

    if results.multi_hand_landmarks != None:
        maingauche, maindoite = 0, 0
        imageHeight, imageWidth, _ = image.shape
        var = 0
        for handLandmarks in results.multi_hand_landmarks:
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (int(handLandmarks.landmark[9].x*500),int(handLandmarks.landmark[9].y*500))
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            var += 1
            image = cv2.putText(image, str(var), org, font,
                                fontScale, color, thickness, cv2.LINE_AA)


    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
