import cv2

image1 = cv2.imread('img/city.jpg')
image2 = cv2.imread('img/grassland.jpg')

image1 = cv2.resize(image1,(640,360))
image2 = cv2.resize(image2,(640,360))

addImage = cv2.addWeighted(image1,0.5,image2,0.6,0)

cv2.imshow('Weighted Image' , addImage)


if cv2.waitKey(0) & 0xff == 27:
    cv2.destoryAllWindows()

