import os
import cv2
import time
import numpy as np


class ImageFilter:
    @staticmethod
    def gray_scale(image):
        B, G , R = cv2.split(image)
        return R

    @staticmethod
    def invert(image):
        return 255 - image

    @staticmethod
    def median_blur(image):
        out = cv2.medianBlur(image,15)
        return out

    @staticmethod
    def sharpen_image(image):
        kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
        out = cv2.filter2D(image,-1,kernel)
        return out

    @staticmethod
    def contrast(image):
        brightness = 5
        contrast = 1.5
        out = cv2.addWeighted(image,contrast,np.zeros(image.shape,image.dtype),0,brightness)
        return out


cap = cv2.VideoCapture(0)

def main():
    sec = 0
    while True:

        ret ,frame = cap.read()

        if not ret:
            print("You can never make it")
            break
        sec += 1

        print(f"\r{sec}",end="")

        cv2.imshow("Camera Feed", ImageFilter.sharpen_image(ImageFilter.contrast(frame)))

        if cv2.waitKey(1)  & 0xFF==ord('q'):
            break
        pass
    pass

main()
