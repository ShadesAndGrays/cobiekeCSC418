import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread('img/grassland.jpg')


plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(image)


inverse_image = 255 - image


cv2.imwrite('img/inverse_image.jpg',inverse_image)

plt.subplot(1,2,2)
plt.title("Inverse color")
plt.imshow(inverse_image)
plt.show()
