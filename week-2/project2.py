import os
import cv2
import time
import numpy as np

root_dir = os.path.abspath(os.curdir) 
class_directory = "img/class" # all profiles are stored here

class ImageFilter:
    @staticmethod
    def prompt():
        choice = input("""
Select a filter:
1. gray_scale
2. invert
3. blur
4. sharpen
5. contrast and brightness
    """)
        match choice := int(choice):
            case 1:
                return ImageFilter.gray_scale
            case 2:
                return ImageFilter.invert
            case 3:
                return ImageFilter.median_blur
            case 4:
                return ImageFilter.sharpen_image
            case 5:
                return ImageFilter.contrast

    @staticmethod
    def gray_scale(image):
        _, _ , out = cv2.split(image)  # bgr
        return out # only take the red channel 

    @staticmethod
    def invert(image,threshold=255):
        out =  threshold - image
        return out

    @staticmethod
    def median_blur(image,blur_amount=15):
        out = cv2.medianBlur(image,blur_amount)
        return out

    @staticmethod
    def sharpen_image(image):
        kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
        out = cv2.filter2D(image,-1,kernel)
        return out

    @staticmethod
    def contrast(image,brightness = 5,contrast = 1.5):
        out = cv2.addWeighted(image,contrast,np.zeros(image.shape,image.dtype),0,brightness)
        return out

def main():
    print("Welcome to stutent effects")
    username = input("input username: ")
    matno = input("input mat no: ")
    path = f"{root_dir}/{class_directory}/{username}.jpeg" 
    if os.path.exists(path):
        img = cv2.imread(path)
        filter = ImageFilter.prompt()
        if filter == None:
            return
        img = filter(img)
        output_path = f"{root_dir}/{class_directory}/{username}_render.jpeg"
        cv2.imwrite(output_path,img)
        print(output_path,"generated")
        cv2.imshow(f"{username}: {matno}",img)
        cv2.waitKey(0)

    else:
        print("user does not exist")
        pass

main()
