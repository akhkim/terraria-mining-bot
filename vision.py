import cv2 as cv
import numpy as np
from hsvfilter import HsvFilter


class Vision:

    def __init__(self, needle_img_path, method = cv.TM_CCOEFF_NORMED):
        if needle_img_path:
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]
 
        self.method = method
        
    def find(self, haystack_img, threshold=0.65, max_results = 50):
        
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        if not locations:
            return np.array([], dtype = np.int32).reshape(0, 4)
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        if len(rectangles) > max_results:
            print("Warning: too many results, raise the threshold.")
            rectangles = rectangles[:max_results]

        return rectangles
    
    def get_click_points(self, haystack_img, rectangles, debug_mode=None):
        points = []
        for (x, y, w, h) in rectangles:

            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x, center_y))
        
        return points
    
    def draw_rectangles(self, haystack_img, rectangles):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                            lineType=line_type, thickness=2)
            
            return haystack_img
        
    def draw_crosshairs(self, haystack_img, points):
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img
    
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizedWindow(self.TRACKBAR_WINDOW, 350, 700)

        def nothing(position):
            pass

        cv.createTrackbar("HMin", self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar("SMin", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar("VMin", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar("HMax", self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar("SMax", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar("VMax", self.TRACKBAR_WINDOW, 0, 255, nothing)

        cv.setTrackbarPos("HMax", self.TRACKBAR_WINDOW, 0, 179)
        cv.setTrackbarPos("SMax", self.TRACKBAR_WINDOW, 0, 255)
        cv.setTrackbarPos("VMax", self.TRACKBAR_WINDOW, 0, 255)

        cv.createTrackbar("SAdd", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar("SSub", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar("VAdd", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar("VSub", self.TRACKBAR_WINDOW, 0, 255, nothing)

    def get_hsv_filter_from_controls(self):
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos("HMin", self.TRACKBAR_WINDOW)
        hsv_filter.hMin = cv.getTrackbarPos("SMin", self.TRACKBAR_WINDOW)
        hsv_filter.hMin = cv.getTrackbarPos("VMin", self.TRACKBAR_WINDOW)
        hsv_filter.hMin = cv.getTrackbarPos("HMax", self.TRACKBAR_WINDOW)
        hsv_filter.hMin = cv.getTrackbarPos("SMax", self.TRACKBAR_WINDOW)
        hsv_filter.hMin = cv.getTrackbarPos("VMax", self.TRACKBAR_WINDOW)
        hsv_filter.hMin = cv.getTrackbarPos("SAdd", self.TRACKBAR_WINDOW)
        hsv_filter.hMin = cv.getTrackbarPos("SSub", self.TRACKBAR_WINDOW)
        hsv_filter.hMin = cv.getTrackbarPos("VAdd", self.TRACKBAR_WINDOW)
        hsv_filter.hMin = cv.getTrackbarPos("VSub", self.TRACKBAR_WINDOW)
        return hsv_filter
    
    def apply_hsv_filter(self, original_image, hsv_filter = None):
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(s, hsv_filter.vAdd)
        v = self.shift_channel(s, -hsv_filter.vSub)
        hsv = cv.merge((h, s, v))

        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask = mask)

        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)
        return img
    
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            lim = -amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c