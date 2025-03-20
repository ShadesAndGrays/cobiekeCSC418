import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread('img/city.jpg')

plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(image)

kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])

sharpened_image = cv2.filter2D(image,-1,kernel)

cv2.imwrite('img/sharpened_image.jpg',sharpened_image)

plt.subplot(1,2,2)
plt.title("Sharpening")
plt.imshow(sharpened_image)
plt.show()
