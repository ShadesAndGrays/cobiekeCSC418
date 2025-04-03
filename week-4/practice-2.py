import cv2
import numpy as np

image = cv2.imread('img/wole.jpg',cv2.IMREAD_GRAYSCALE)

image = cv2.resize(image,(500,400))

kernel_x = np.array([
    [-1,-1,-1],
    [ 0, 0, 0],
    [ 1, 1, 1],
    ])

kernel_y = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1],
    ])
perwitt_x = cv2.filter2D(image,-1,kernel_x)
perwitt_y = cv2.filter2D(image,-1,kernel_y)

perwitt_combined = np.sqrt(np.square(perwitt_x)+np.square(perwitt_y))

cv2.imshow('Original',image)
cv2.imshow('Perwitt Edges',np.uint8(perwitt_combined))

cv2.waitKey(0)
cv2.destroyAllWindows()
