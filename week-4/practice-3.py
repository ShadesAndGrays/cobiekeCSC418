import cv2
import numpy as np

image = cv2.imread('img/wole.jpg',cv2.IMREAD_GRAYSCALE)

image = cv2.GaussianBlur(image,(5,5),0)

kernel_x = np.array([
    [ 1, 0],
    [ 0,-1],
    ])

kernel_y = np.array([
    [-1, 0],
    [ 0, 1],
    ])


robert_x = cv2.filter2D(image,-1,kernel_x)
robert_y = cv2.filter2D(image,-1,kernel_y)

robert_combined = np.sqrt(np.square(robert_x)+np.square(robert_y))

cv2.imshow('Original',image)
cv2.imshow('Robert Edges',np.uint8(robert_combined))

cv2.waitKey(0)
cv2.destroyAllWindows()
