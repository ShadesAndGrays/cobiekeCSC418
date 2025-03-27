import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

img = cv.imread('img/city.jpg')

plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(img)

cropped_img = img[50:200, 50:80] # px (50 - 200, y axis) 50 - 80 

# This crops only the door image out
plt.subplot(1,2,2)
plt.title("Cropped Image")
plt.imshow(cropped_img)

plt.show()
cv.imwrite('img/cropped_out.jpg',cropped_img) #
cv.waitKey(0)
cv.destroyAllWindows()
