import numpy as np
import cv2 as cv
import win32gui
import win32ui
import win32con
import setup

class WindowCapture:
    def __init__(self):
        for window in list_window():
            window_text = win32gui.GetWindowText(window)
            if window_text.startswith("Terraria: "):
                window_name = window_text
        
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception("Terraria not found.")
        
        if setup.windowed_borderless:
            self.w = setup.game_width
            self.h = setup.game_height
            self.frame = (0, 0)
        else:
            self.w = setup.game_width - 24
            self.h = setup.game_height - 63
            self.frame = (12, 51)
        

    def get_screenshot(self):
        
        bmpfilenamename = "out.bmp"
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, self.frame, win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype="uint8")
        img.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = np.ascontiguousarray(img[..., :3])
        return img


def list_window():
    windows = []
    def winEnumHandler(hwnd, ctx):
        ctx.append(hwnd)
    win32gui.EnumWindows(winEnumHandler, windows)
    return windows