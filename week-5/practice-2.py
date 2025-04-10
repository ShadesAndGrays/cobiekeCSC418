import cv2
from matplotlib import pyplot as plt

img = cv2.imread("img/friends.jpg")


img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)


face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

found = face_data.detectMultiScale(img_gray, minSize=(20,20))

amound_found = len(found)


if amound_found != 0:
    print(found)
    for (x,y,width,height) in found:
        cv2.rectangle(img_rgb,(x,y),
                     (x + height,y + width), (0,255,0),5)

plt.subplot(1,1,1)
plt.imshow(img_rgb)
plt.show()
