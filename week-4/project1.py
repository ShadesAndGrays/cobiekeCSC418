import cv2
import time
import numpy as np


class ImageFilter:
    @staticmethod
    def Sobel(image):

        sobel_x = cv2.Sobel(image,cv2.CV_64F, 1,0,ksize=3)
        sobel_y = cv2.Sobel(image,cv2.CV_64F, 0,1,ksize=3)

        sobel_combined = cv2.magnitude(sobel_x,sobel_y)/(64*16)
        return sobel_combined

    @staticmethod
    def Perwitt(image):
        kernel_x = np.array([
            [-1,-1,-1],
            [ 0, 0, 0],
            [ 1, 1, 1],
            ])

        kernel_y = np.array([
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1],
            ])
        perwitt_x = cv2.filter2D(image,-1,kernel_x)
        perwitt_y = cv2.filter2D(image,-1,kernel_y)

        perwitt_combined = np.sqrt(np.square(perwitt_x)+np.square(perwitt_y))
        return np.uint8(perwitt_combined)

    @staticmethod
    def Robert(image):
        image = cv2.GaussianBlur(image,(5,5),0)

        kernel_x = np.array([
            [ 1, 0],
            [ 0,-1],
            ])

        kernel_y = np.array([
            [-1, 0],
            [ 0, 1],
            ])


        robert_x = cv2.filter2D(image,-1,kernel_x)
        robert_y = cv2.filter2D(image,-1,kernel_y)

        robert_combined = np.sqrt(np.square(robert_x)+np.square(robert_y))

        return np.uint8(robert_combined)

    @staticmethod
    def Laplacian(image):
        laplacian = cv2.Laplacian(image,cv2.CV_64F)
        laplacian = cv2.convertScaleAbs(laplacian)

        return np.uint8(laplacian)

    @staticmethod
    def Canny(image):
        # image min and max
        edges = cv2.Canny(image,100,170)
        return edges


cap = cv2.VideoCapture(0)

def main():
    while True:

        ret ,frame = cap.read()
        B, G , frame = cv2.split(frame)

        if not ret:
            print("You can never make it")
            # break

        cv2.imshow("Camera Feed", ImageFilter.Canny(frame))
        if cv2.waitKey(100)  & 0xFF==ord('q'):
            break
        pass
    pass

main()
