import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

img = cv.imread('img/city.jpg')

plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(img)

(rows, cols,_) = img.shape

M = np.float32(np.array([[1,0,0],[0,-1,rows],[0,0,1]]))

reflected_img = cv.warpPerspective(img,M,(int(cols),int(rows)))

plt.subplot(1,2,2)
plt.title("Reflected Image")
plt.imshow(reflected_img)

plt.show()

cv.imwrite('img/reflection_out.jpg',reflected_img)
cv.waitKey(0)
cv.destroyAllWindows()

