import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('img/city.jpg')

# cv.imshow('Original Image',img)
# cv.waitKey(0)
plt.subplot(2,2,1)
plt.title("Original")
plt.imshow(img)

gaussian = cv.GaussianBlur(img,(7,7),0)
# cv.imshow('Gaussian Blurring',gaussian)
# cv.waitKey(0)
plt.subplot(2,2,2)
plt.title("Gaussian Blurring")
plt.imshow(gaussian)


median =cv.medianBlur(img,5)
# cv.imshow('Median Blurring',median)
# cv.waitKey(0)
plt.subplot(2,2,3)
plt.title("Median Blurring")
plt.imshow(median)

bilateral = cv.bilateralFilter(img,9,75,75)
# cv.imshow('Bilateral Blurring',bilateral)
# cv.waitKey(0)
plt.subplot(2,2,4)
plt.title("Bilateral Blurring")
plt.imshow(bilateral)

plt.show()
cv.waitKey(0)
cv.destroyAllWindows()

