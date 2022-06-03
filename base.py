import cv2
import mediapipe as mp
import serial

ser = serial.Serial('COM3', 9600)

r, g, b, k = 0 ,0, 0 ,0
lum = 200
maindoite = 0
maingauche = 0
red, green, blue= 100, 100, 100

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def rgbcolor(yo):
    global r, g, b, k

    yo = int(yo)
    if (0<=yo<=255):
        hx = hex(yo)[2::]
        if (yo<16):
            v= "0"
            hx = "%s%s" % (v, hx)
        k = "#ff"
        k = "%s%s" % (k, hx)
        bv = "00"
        k = "%s%s" % (k, bv)
        r = 255
        g = yo
        b = 0

    if (256<=yo<=511):
        yo = 511 - yo
        hx = hex(yo)[2::]
        if (yo<16):
            v= "0"
            hx = "%s%s" % (v, hx)
        k = "#"
        k = "%s%s" % (k, hx)
        bv = "ff00"
        k = "%s%s" % (k, bv)
        r = yo
        g = 255
        b = 0

    if (512 <= yo <= 767):
        yo = yo - 512
        hx = hex(yo )[2::]
        if (yo<16):
            v= "0"
            hx = "%s%s" % (v, hx)

        k = "#00ff"
        k = "%s%s" % (k, hx)
        bv = ""
        k = "%s%s" % (k, bv)
        r = 0
        g = 255
        b = yo

    if (768 <= yo <= 1023):
        yo = 1023 -yo
        hx = hex(yo )[2::]
        if (yo<16):
            v= "0"
            hx = "%s%s" % (v, hx)

        k = "#00"
        k = "%s%s" % (k, hx)
        bv = "ff"
        k = "%s%s" % (k, bv)
        r = 0
        g = yo
        b = 255

    if (1024 <= yo <= 1279):
        yo = yo - 1024
        hx = hex(yo)[2::]
        if (yo<16):
            v= "0"
            hx = "%s%s" % (v, hx)

        k = "#"
        k = "%s%s" % (k, hx)
        bv = "00ff"
        k = "%s%s" % (k, bv)
        r = yo
        g = 0
        b = 255

    if (1278 <= yo <= 1535):
        yo = 1535 - yo
        hx = hex(yo )[2::]
        if (yo<16):
            v= "0"
            hx = "%s%s" % (v, hx)
        k = "#ff00"
        k = "%s%s" % (k, hx)
        bv = ""
        k = "%s%s" % (k, bv)
        r = 255
        g = 0
        b = yo

    if (1536<= yo):
        k = "#ffffff"
        r = 255
        g = 255
        b = 255
    return r, g, b, k


# For static images:
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=8,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))

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
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
      #r, g, b, k = rgbcolor(int(results.multi_hand_landmarks.handLandmarks.landmark[12].y * 1540))
      #print(r, g, b)
      if results.multi_hand_landmarks != None:
          maingauche, maindoite = 0, 0
          imageHeight, imageWidth, _ = image.shape
          for handLandmarks in results.multi_hand_landmarks:
              for point in mp_hands.HandLandmark:
                  normalizedLandmark = handLandmarks.landmark[point]
                  pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                            normalizedLandmark.y,
                                                                                            imageWidth, imageHeight)




          if 0<= handLandmarks.landmark[12].y <= 1 :
              rgbcolor(int(handLandmarks.landmark[12].y * 1540))
              red = r
              blue = b
              green = g
              if int(red) < 10:
                  red = '00{}'.format(red)
              elif 10 <= int(red) < 100:
                  red = '0{}'.format(red)
              if int(blue) < 10:
                  blue = '00{}'.format(blue)
              elif 10 <= int(blue) < 100:
                  blue = '0{}'.format(blue)
              if int(green) < 10:
                  green = '00{}'.format(green)
              elif 10 <= int(green) < 100:
                  green = '0{}'.format(green)




              if handLandmarks.landmark[9].y < handLandmarks.landmark[0].y:
                  if handLandmarks.landmark[12].y < handLandmarks.landmark[9].y:
                      majeur = handLandmarks.landmark[9].y - handLandmarks.landmark[12].y
                      pouce = handLandmarks.landmark[1].y - handLandmarks.landmark[5].y
                      lum = int(majeur / pouce * 255)
                      if lum > 253:
                          lum = 255
                      if lum < 1 :
                          lum = 1
                  if handLandmarks.landmark[12].y > handLandmarks.landmark[9].y:
                      lum = 0
              if handLandmarks.landmark[9].y > handLandmarks.landmark[0].y:
                  if handLandmarks.landmark[12].y > handLandmarks.landmark[9].y:
                      majeur = handLandmarks.landmark[12].y - handLandmarks.landmark[9].y
                      pouce = handLandmarks.landmark[5].y - handLandmarks.landmark[1].y
                      lum = int(majeur / pouce * 200)
                      if lum > 200:
                          lum = 200
                      if lum < 1 :
                          lum = 1
                  if handLandmarks.landmark[12].y < handLandmarks.landmark[9].y:
                      lum = 0
              color = '{}{}{}{}'.format(red, green, blue, lum)
              ser.write(bytes(color, 'utf-8'))





    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()