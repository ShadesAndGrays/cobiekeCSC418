import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

image = cv2.imread('img/lake.jpg')


gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


faces = face_cascade.detectMultiScale(gray_image,scaleFactor=1.3,minNeighbors=5,minSize=(10,30))

for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y), (x+w,y+y),(0,255,0),2)

cv2.imshow('Face Detection',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
