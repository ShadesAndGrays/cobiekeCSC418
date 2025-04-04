import cv2

image = cv2.imread('img/wole.jpg',cv2.IMREAD_GRAYSCALE)

image = cv2.resize(image,(500,400))

edges = cv2.Canny(image,100,200)

cv2.imshow('Original',image)
cv2.imshow('Canny Edges',edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
