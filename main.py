from time import time
from windowcapture import WindowCapture
from vision import Vision
import numpy as np
import cv2 as cv
import pyautogui
import setup


wincap = WindowCapture()

# Cascade version
cascade_ore = cv.CascadeClassifier("cascade/" + setup.target_ore + setup.spelunker + "_spelunker/cascade.xml")
vision_ore = Vision(None)

loop_time = time()
while True:
    screenshot = wincap.get_screenshot()
    rectangles = cascade_ore.detectMultiScale(screenshot)
    detection_image = vision_ore.draw_rectangles(screenshot, rectangles)

    cv.imshow("Matches", detection_image)

    key = cv.waitKey(1)
    if key == ord("q"):
        cv.destroyAllWindows()
        break
    elif key == ord("f"):
        cv.imwrite("./images/" + setup.target_ore + setup.spelunker + "_spelunker/positive/{}.jpg".format(loop_time), screenshot)
    elif key == ord("d"):
        cv.imwrite("./images/" + setup.target_ore + setup.spelunker + "_spelunker/negative/{}.jpg".format(loop_time), screenshot)



# HSV detection
# from hsvfilter import HsvFilter

# vision_ore = Vision("ore_processed.jpg")
# vision_ore.init_control_gui()
# hsv_filter = HsvFilter(0, 180, 129, 15, 229, 243, 143, 0, 67, 0)

# loop_time = time()
# while(True):
#     screenshot = wincap.get_screenshot()
#     processed_image = vision_ore.apply_hsv_filter(screenshot, hsv_filter)
#     rectangles = vision_ore.find(processed_image, 0.46)
#     output_image = vision_ore.draw_rectangles(screenshot, rectangles)

#     cv.imshow('Processed', processed_image)
#     cv.imshow('Matches', output_image)

#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break
