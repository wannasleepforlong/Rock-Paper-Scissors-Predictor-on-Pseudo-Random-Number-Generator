import back_end as be

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

import pygame


TIME_TO_START = 3

back_end = be.BackEnd

pygame.mixer.init()
pygame.mixer.music.load("files/battle.mp3")
pygame.mixer.music.play(-1)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1, detectionCon=0.3, minTrackCon=0.5)  # Todo:  check for other values too

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]

while True:
    imgBG = cv2.imread("files/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    hands, img = detector.findHands(imgScaled)

    imgAI = cv2.imread(f'files/{0}.png', cv2.IMREAD_UNCHANGED)
    if startGame:

        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > TIME_TO_START:
                stateResult = True
                timer = 0

                if hands:
                    player_move = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        player_move = 0
                        print("Rock")
                    if fingers == [1, 1, 1, 1, 1]:
                        player_move = 1
                        print("Paper")
                    if fingers == [0, 1, 1, 0, 0]:
                        player_move = 2
                        print("Scissors")

                    # Used for finding showing computer decisions
                    computer_move, model_choice = back_end.choose_computer_move()
                    imgAI = cv2.imread(f'files/{computer_move+1}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    back_end.update_value(player_move, computer_move, model_choice=model_choice)  # Used for saving data
                    scores[0], scores[1] = back_end.get_scores()

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
