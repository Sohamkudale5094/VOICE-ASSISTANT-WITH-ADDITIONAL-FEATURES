import time
import pyautogui

import cv2 as cv
import numpy as np
import mediapipe as mp

class VirtualMouse:
    # initiating live video camera
    def  initializeCam(self):
        # starts capturing real image
        cap = cv.VideoCapture(0)
        # find hand in frame
        detectHand = mp.solutions.hands.Hands()
        drawing_utils = mp.solutions.drawing_utils
        screen_width, screen_height = pyautogui.size()
        indexFing_y = 0
        midleFing_y = 0
        while True:
            # make a frame for gesture 
            ret, frame = cap.read()
            frame = cv.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            # convert to RGB
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            # find landmarks onto the palm
            mark = detectHand.process(rgb_frame)
            handLandmark = mark.multi_hand_landmarks
            
            if handLandmark :
                for hand in handLandmark :
                    drawing_utils.draw_landmarks(frame, hand)
                    landmarks = hand.landmark
                    for id, landmark in enumerate(landmarks):
                        x = int(landmark.x * frame_width)
                        y = int(landmark.y * frame_height)

                        # accessing only index finger
                        if id == 8:
                            # build a circle on index finger
                            cv.circle(img=frame, center=(x,y), radius=10, color=(0,255,0))
                            # retrieving positions of index finger 
                            indexFing_x = (screen_width/frame_width) * x
                            indexFing_y = (screen_height/frame_height) * y
                         # accessing only midle finger
                        if id == 12:
                            # build a circle on midle finger
                            cv.circle(img=frame, center=(x,y), radius=10, color=(0,255,0))
                            # retrieving positions of midle finger 
                            midleFing_x = (screen_width/frame_width) * x
                            midleFing_y = (screen_height/frame_height) * y
                            # move cursor with index finger
                            pyautogui.moveTo(midleFing_x, midleFing_y)
                            if (abs(indexFing_x - midleFing_x) < 20):
                                pyautogui.doubleClick()
                        # accessing only thumb
                        if id == 4:
                            # build a circle on thumb
                            cv.circle(img=frame, center=(x,y), radius=10, color=(0,255,0))
                            # retrieving positions of thumb
                            thumb_x = (screen_width/frame_width) * x
                            thumb_y = (screen_height/frame_height) * y
                            # move cursor with index finger
                            if (abs(indexFing_y - thumb_y) < 30) :
                               pyautogui.click(button='left')
                               time.sleep(1)
                            if (abs(midleFing_y - thumb_y) < 30) :
                               pyautogui.click(button='right')
                               time.sleep(1)
                     #print(handLandmark)
          
            cv.imshow("Luci's Virtual Mouse Window",frame)
            cv.waitKey(1)

            # accept key from user
            key = cv.waitKey(1)
            # if esc key is pressed, destroy window & terminate execution
            if key == 27:
                cv.destroyWindow("Luci's Virtual Mouse Window")
                break

#-----driver code-----
obj = VirtualMouse()                                 # creating object
obj.initializeCam()                                     # call internal function
    
