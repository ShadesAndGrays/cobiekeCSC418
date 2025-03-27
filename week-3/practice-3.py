import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

img = cv.imread('img/city.jpg')
(rows, cols,_) = img.shape

plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(img)


origin = (cols/2,rows/2)
img_rotation = cv.warpAffine(img,cv.getRotationMatrix2D(origin,30,0.6),(cols,rows))


plt.subplot(1,2,2)
plt.title("Rotated image")
plt.imshow(img_rotation)

plt.show()

cv.imwrite('img/rotation_out.jpg',img_rotation)
cv.waitKey(0)
cv.destroyAllWindows()
