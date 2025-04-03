import cv2
import numpy as np

image = cv2.imread('img/wole.jpg',cv2.IMREAD_GRAYSCALE)

image = cv2.resize(image,(500,400))

laplacian = cv2.Laplacian(image,cv2.CV_64F)
laplacian = cv2.convertScaleAbs(laplacian)


cv2.imshow('Original',image)
cv2.imshow('Sobel Edges',np.uint8(laplacian))

cv2.waitKey(0)
cv2.destroyAllWindows()
