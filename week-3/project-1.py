"""
criteria:
    valid email
    18 years above
    choice of collection
collection/category:
    traditional
    modern
    contemporary

-- Login

-- Input category

-- List image from each category

-- Select image

-- Select transformation

-- Apply transformation

-- Display image 

-- Save image 

"""

import json
from enum import Enum
import os
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


class Collection(Enum):
    TRADITIONAL = 1
    MODERN = 2
    CONTEMPORARY = 3

class ImageTransformer:
    @staticmethod
    def select_transfomer():
        choice = int(input ("""
Available Transformation
    1) gaussian blur
    2) median blur
    3) bilateral blur
    4) shear-y
    5) shear-x
    6) crop
    7) reflect
    8) rotate
    9) traslate
Select Transformation
              """)) 
        match choice:
            case 1:
                return ImageTransformer.gaussian_blur
            case 2:
                return ImageTransformer.median_blur
            case 3:
                return ImageTransformer.bilateral_blur
            case 4:
                return ImageTransformer.shear_y
            case 5:
                return ImageTransformer.shear_x
            case 6:
                return ImageTransformer.crop
            case 7:
                return ImageTransformer.refelct
            case 8:
                return ImageTransformer.rotate
            case 9:
                return ImageTransformer.translate
            case _:
                return ImageTransformer.translate

    @staticmethod
    def gaussian_blur(img):
        width = int(input("Kernel width: "))
        height = int(input("Kernel height: "))
        output = cv.GaussianBlur(img,(width,height),0)
        return output

    @staticmethod
    def median_blur(img):
        amount = int(input("blur amount(1-10): "))
        output = cv.medianBlur(img,amount)
        return output

    @staticmethod
    def bilateral_blur(img):
        diameter = int(input("blur diameter(1-10): "))
        output = cv.bilateralFilter(img,diameter,75,75)
        return output

    @staticmethod
    def shear_y(img):
        (cols,rows,_) = img.shape
        shear_amount = np.float32(input("Shear amount(0.0 - 1.0): "))
        scale = np.float32(input("Scale: "))
        M = np.float32(np.array([[1,0,0],[shear_amount,1,0],[0,0,1]]))
        output = cv.warpPerspective(img,M,(int(cols*scale),int(rows*scale)))
        return output

    @staticmethod
    def shear_x(img):
        (cols,rows,_) = img.shape
        scale = np.float32(input("Scale: "))
        shear_amount = np.float32(input("Shear amount(0.0 - 1.0): "))
        M = np.float32(np.array([[1,shear_amount,0],[0,1,0],[0,0,1]]))
        output = cv.warpPerspective(img,M,(int(cols*scale),int(rows*scale)))
        return output

    @staticmethod
    def crop(img):
        x_begin = int(input("Top Left(x): "))
        y_begin = int(input("Top Left(y): "))
        x_end = int(input("Bottom Right(x): "))
        y_end = int(input("Bottom Right(y): "))

        output = img[y_begin:y_end, x_begin:x_end] # px (50 - 200, y axis) 50 - 80 
        return output

    @staticmethod
    def rotate(img):
         
        degree = int(input("Degree: "))
        scale = int(input("Scale: "))
        (cols,rows,_) = img.shape
        origin = (cols/2,rows/2)
        output = cv.warpAffine(img,cv.getRotationMatrix2D(origin,degree,scale),(cols,rows))
        return output

    @staticmethod
    def refelct(img):
        (cols,rows,_) = img.shape
        M = np.float32(np.array([[1,0,0],[0,-1,rows],[0,0,1]]))
        output = cv.warpPerspective(img,M,(int(cols),int(rows)))
        return output

    @staticmethod
    def translate(img):
        (cols,rows,_) = img.shape
        x = int(input(" traslate x: "))
        y = int(input(" traslate y: "))
        M = np.float32(np.array([[1,0,x],[0,1,y]]))
        output = cv.warpAffine(img,M,(cols,rows))
        return output

class User:
    def __init__(self,id,email,password) -> None:
        self.id = id
        self.email = email
        self.password = password

    def validate(self,email,password):
        return self.email == email and self.password == password

def login(email) -> int:
    password = input("Password: ")
    with open('img/museum/auth.json','r') as file:
        auth = json.load(file) # load credentials
        for user in [User(x['id'],x["email"],x["password"]) for x in auth]: # cast and iterate
            if email == user.email:
                if password == user.password:
                    return user.id
                else:
                    print("Invalid password")
                    return -1
    print("User does not exist")
    return -1

def prompt_category():
    choice  = int(input("""
Select a collection to view
    1) Traditional
    2) Modern
    3) Contemporary

Select a collection: """))

    return Collection(choice)


def get_museum_collection_files(collection:Collection):
    sub_path = collection.name.lower()
    files = os.listdir(f"./img/museum/{sub_path}") # get file in sub dir
    return [f"./img/museum/{sub_path}/{file}" for file in files] # remap to relative dir

def select_from_path_list(paths):
    for i in range(len(paths)):
        p:str = paths[i]
        print(i+1,p.split("/")[-1] ) # get last name of file from path
    return paths[int(input("Pick file: "))- 1]

def display_samlples(paths):
    print("Displaying samples")
    for i in range(0,min(len(paths),4)):
        img = cv.imread(paths[i])
        plt.subplot(2,2,i+1)
        plt.title(((paths[i].split("/")[-1]).split(".")[0]).replace('-',' '))
        plt.imshow(img)
    plt.show()
    cv.waitKey(0)
    cv.destroyAllWindows()

def display_trasform(image_files):
    file = select_from_path_list(image_files)
    img = cv.imread(file)
    transformation = ImageTransformer.select_transfomer()
    img = transformation(img)
    
    plt.subplot(1,1,1)
    file_name = (file.split("/")[-1]).split(".")[0]
    formated_name = file_name.replace('-',' ') 
    plt.title(f"{formated_name} {transformation.__name__.replace('_',' ').capitalize()}")
    plt.imshow(img)
    plt.show()
    cv.imwrite(f"{file_name}-{transformation.__name__}.jpg",img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def main():
    email = input("Enter you email: ")
    user_id = login(email)
    if user_id < 0: # user does not exist
        return 

    category = prompt_category()

    category_files = get_museum_collection_files(category)

    if len(category_files) <= 0:
        print("Category is unavalible")
        return

    if input("show samples(y/N): ").lower() == 'y': 
        display_samlples(category_files)
    display_trasform(category_files)

main()
