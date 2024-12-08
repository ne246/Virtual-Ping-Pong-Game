import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

capture = cv2.VideoCapture(0)
capture.set(3, 1280)
capture.set(4, 720)

# Importing all images
imgBackground = cv2.imread("Resources/Background.png")
imgGameOver = cv2.imread("Resources/gameOver.png")
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)

# Hand Dectector
detector = HandDetector(detectionCon = 0.8, maxHands = 2)

# Varibles 
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False
score = [0, 0]

while True:
    _, camera = capture.read()
    camera = cv2.flip(camera, 1)
    cameraRaw = camera.copy()

    # Find the hand and its landmarks
    hands, camera = detector.findHands(camera, flipType = False)                      # with draw  (if you dont want the drawings of the hand add (,draw = False) and remove camera varible)

    # Overlaying the background image
    camera = cv2.addWeighted(camera, 0.2, imgBackground, 0.5, 0)

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']

            h1, w1, _ = imgBat1.shape
            y1 = y - h1//2
            y1 = np.clip(y1, 20, 415)


            if hand['type'] == "Left":
                camera = cvzone.overlayPNG(camera, imgBat1, (59, y1))
                if  59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1
            
            if hand['type'] == "Right":
                camera = cvzone.overlayPNG(camera, imgBat2, (1195, y1))
                if  1195-50 < ballPos[0] < 1195 + w1 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1

    #Game Over
    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

    if gameOver:
        camera = cv2.addWeighted(camera, 0.2, imgGameOver, 0.5, 0)
        cv2.putText(camera, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)

    # If game not over move the ball
    else:
    # Move the ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY
                                    

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Draw the ball
        camera = cvzone.overlayPNG(camera, imgBall, ballPos)

        cv2.putText(camera, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(camera, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    camera[580:700, 20:233] = cv2.resize(cameraRaw, (213, 120))

    #shows camera
    cv2.imshow('Ping Pong', camera)
    if cv2.waitKey(1) == ord('q'):
        break
    
    if cv2.waitKey(1) == ord('r'):
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("Resources/gameOver.png")
