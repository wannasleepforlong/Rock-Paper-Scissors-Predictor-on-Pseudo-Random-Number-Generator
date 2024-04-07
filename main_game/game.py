import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

import pygame


TIME_TO_START = 3


pygame.mixer.init()
pygame.mixer.music.load("files/battle.mp3")
pygame.mixer.music.play(-1)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1,detectionCon=0.3, minTrackCon=0.5) # Todo:  check for other values too

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]

while True:
    imgBG = cv2.imread("files/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if hands:  # TODO: for testing Delete this
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        if fingers == [0, 0, 0, 0, 0]:
            print("Rock")
        if fingers == [1, 1, 1, 1, 1]:
            print("Paper")
        if fingers == [0, 1, 1, 0, 0]:
            print("Scissors")

    if startGame:

        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
 
            if timer > TIME_TO_START:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                        print("Rock")
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                        print("Paper")
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3
                        print("Scissors")

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'files/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
 
                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

                    # draw
                    if playerMove == randomNumber:
                        pass

                    else:
                        pass

    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Scaled", imgScaled)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    elif key == ord('q'):
        startGame = False
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
pygame.mixer.quit()
