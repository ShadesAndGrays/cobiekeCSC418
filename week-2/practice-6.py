import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread('img/city.jpg')


plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(image)


# scaled_image = cv2.resize(image,None,fx=2,fy=2)
scaled_image = cv2.resize(image,None,fx=4,fy=4)

cv2.imwrite('img/ScaledImage.jpg',scaled_image)

plt.subplot(1,2,2)
plt.title("scaled")
plt.imshow(scaled_image)
plt.show()
