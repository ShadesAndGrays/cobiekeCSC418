import os
import cv2
import time
import numpy as np

root_dir = os.path.abspath(os.curdir) 
class_directory = "img/class" # all profiles are stored here

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

def main():
    img = cv2.imread("img/grassland.jpg")
    cv2.imshow("File",ImageFilter.median_blur(img))
    cv2.waitKey(10000) 
    pass

main()
