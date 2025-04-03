import cv2
import numpy as np

image = cv2.imread('img/wole.jpg',cv2.IMREAD_GRAYSCALE)

image = cv2.resize(image,(500,400))

sobel_x = cv2.Sobel(image,cv2.CV_64F, 1,0,ksize=3)
sobel_y = cv2.Sobel(image,cv2.CV_64F, 0,1,ksize=3)

sobel_combined = cv2.magnitude(sobel_x,sobel_y)

cv2.imshow('Original',image)
cv2.imshow('Sobel Edges',np.uint8(sobel_combined))

cv2.waitKey(0)
cv2.destroyAllWindows()
