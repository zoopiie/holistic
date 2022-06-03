import cv2
import serial

ser = serial.Serial('COM5', 9600)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


droite = "090"
gauche = "090"
pince = "090"
rot = "090"

var = 1

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    max_num_hands=1,
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
        print('')
        """mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style())"""

      if results.multi_hand_landmarks != None:
          if len(results.multi_hand_landmarks) > 1:
              var = 0
          for handLandmarks in results.multi_hand_landmarks:
              """if var == 0:
                  if 0 <= handLandmarks.landmark[12].y <= 1:
                      rot = int(handLandmarks.landmark[12].y * 150)
                      if rot < 0:
                          rot = 0
                      if rot > 150:
                          rot = 150
                      if rot < 10:
                          rot = '00{}'.format(rot)
                      elif 10 <= rot < 100:
                          rot = '0{}'.format(rot)
                  var = 1"""

          if 0<= handLandmarks.landmark[12].y <= 1 :
              gauche = int(handLandmarks.landmark[12].y*100)
              if gauche < 0:
                  gauche = 0
              if gauche > 90:
                  gauche = 90
              gauche = 180 - gauche
              if gauche < 10:
                  gauche = '00{}'.format(gauche)
              elif 10 <= gauche < 100:
                  gauche = '0{}'.format(gauche)

          if 0 <= handLandmarks.landmark[12].x <= 1:
              droite = int((1 - handLandmarks.landmark[12].x )* 100)
              if droite < 0:
                  droite = 0
              if droite > 100:
                  droite = 100
              droite = 180 - droite
              if droite < 10:
                  droite = '00{}'.format(droite)
              elif 10 <= droite < 100:
                  droite = '0{}'.format(droite)

      if handLandmarks.landmark[9].y < handLandmarks.landmark[0].y:
          if handLandmarks.landmark[12].y < handLandmarks.landmark[9].y:
              pince = "090"
          if handLandmarks.landmark[12].y > handLandmarks.landmark[9].y:
              pince = "000"
      if handLandmarks.landmark[9].y > handLandmarks.landmark[0].y:
          if handLandmarks.landmark[12].y > handLandmarks.landmark[9].y:
              pince = "090"
          if handLandmarks.landmark[12].y < handLandmarks.landmark[9].y:
              pince = "000"


      bras = '{}{}{}{}'.format(droite, gauche, rot, pince)
      ser.write(bytes(bras, 'utf-8'))

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
