import cv2 

path = 'img/Nezuko.jpeg'

img = cv2.imread(path) # read image from path

window_name = f'Display Image - {path}'

cv2.imshow(window_name,img) # create window

cv2.waitKey(10000) # wait 10 sec (10000msec) before closing image

cv2.destroyAllWindows()
