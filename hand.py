import cv2
import mediapipe
from led import rgbcolor

drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands


i = 0
with handsModule.Hands(static_image_mode=True) as hands:
    image = cv2.imread("twohands.jpg")
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    imageHeight, imageWidth, _ = image.shape

    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:

            for point in handsModule.HandLandmark:
                normalizedLandmark = handLandmarks.landmark[point]
                pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                          normalizedLandmark.y,
                                                                                          imageWidth, imageHeight)

            print(handLandmarks.landmark[12].x)