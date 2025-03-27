import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

img = cv.imread('img/city.jpg')
rows,cols = img.shape

plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(img)

M = np.float32(np.array([[1,0.5,0],[0,1,0],[0,0,1]]))
sheard_img = cv.warpPerspective(img,M,(int(cols*1.5),int(rows*1.5)))

plt.subplot(1,2,2)
plt.title("Sheard Image")
plt.imshow(sheard_img)

plt.show()

cv.imwrite('img/sheard_img.jpg',sheard_img)
cv.waitKey(0)
cv.destroyAllWindows()
