import cv2

import os

image_path = '/home/shadow/Dev/school_repo/csc-418/week-1/img/Nezuko.jpeg'

directory = r'/home/shadow/Dev/school_repo/csc-418/week-1/img'

img = cv2.imread(image_path,0) # read image in grayscale

os.chdir(directory)

print("Before saving image:")
print(os.listdir(directory))

filename = 'grayImage.jpg'

cv2.imwrite(filename,img)

print("After saving image:")
print(os.listdir(directory))

print("sucessfully saved")


