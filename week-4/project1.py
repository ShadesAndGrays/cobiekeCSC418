from json import load
import cv2
import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from PIL import Image, ImageTk

class ImageFilter:
    @staticmethod
    def Sobel(image):

        sobel_x = cv2.Sobel(image,cv2.CV_64F, 1,0,ksize=3)
        sobel_y = cv2.Sobel(image,cv2.CV_64F, 0,1,ksize=3)

        sobel_combined = cv2.magnitude(sobel_x,sobel_y)
        return np.uint8(sobel_combined)

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


def image_cv_to_tk(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(Image.fromarray(img_rgb))
    return photo

def cv_image_scale(cvimage,size=200):
    scaled_image = cv2.resize(cvimage,(size,size),interpolation=cv2.INTER_LANCZOS4)
    return scaled_image

def main():
    root = tk.Tk()
    root.title("Edge detector")

    edge_detections = {
            "Sobel":  {
                "desc": "Apply Sobel edge detectin",
                "effect":ImageFilter.Sobel,
                },
            "Perwitt": {
                "desc": "Apply Perwitt edge detectin",
                "effect":ImageFilter.Perwitt,
                },
            "Robert":{
                "desc": "Apply Robert edge detectin",
                "effect":ImageFilter.Robert,
                },
            "Laplacian":{
                "desc": "Apply Laplacian edge detection",
                "effect":ImageFilter.Laplacian,
                } ,
            "Canny":{
                "desc": "Apply Canny edge detection",
                "effect":ImageFilter.Canny,
                },
            }

    # set up frames
    filter_frame = tk.Frame(root,background="white")
    filter_frame.pack(side="left",expand=True,fill="both",anchor="w")
    display_frame = tk.Frame(root,background="white")
    display_frame.pack(side="left",expand=True,fill="both",anchor="e")

    # set up image_label
    loaded_image = []
    preview_image = []

    # set up buttons
    select_file_button = ttk.Button(filter_frame,text="Select File")
    select_file_button.bind("<Button-1>",lambda event : set_selected_file())
    select_file_button.pack()
    export_file_button = ttk.Button(display_frame,text="Export Image")
    export_file_button.bind("<Button-1>",lambda event : export_image())
    export_file_button.pack()

    image_label = ttk.Label(display_frame,background="white")
    image_label.pack()

    def update_loaded_img(img):
        nonlocal loaded_image
        nonlocal preview_image
        loaded_image = img 
        scaled_image = cv_image_scale(img)
        preview_image =  image_cv_to_tk(scaled_image)
        image_label.configure(image=preview_image)

    # set up effects list
    effect_list_frame = tk.Frame(filter_frame ,background="white")
    effect_list_frame.pack()
    for i in edge_detections.keys():
        effect_frame = tk.Frame(effect_list_frame,background="white")
        effect_frame.pack()
        label = ttk.Label(effect_frame,text=edge_detections[i]["desc"])
        label.pack()
        button = ttk.Button(effect_list_frame,text=f"Apply {i}")
        button.bind("<Button-1>", lambda event,  effect=edge_detections[i]["effect"]: apply_effect(effect))
        button.pack()

    # apply edge detection
    def apply_effect(filter):
        update_loaded_img(filter(loaded_image))


    def set_selected_file():
        nonlocal loaded_image
        file = filedialog.askopenfilename()
        select_file_button.configure(text=file.split("/")[-1])
        update_loaded_img(cv2.imread(file))

    # export images
    def export_image():
        output_file =  filedialog.asksaveasfilename(filetypes=[("PNG",".png"),("JPEG",".jpg")])
        nonlocal loaded_image
        cv2.imwrite(output_file,loaded_image)

    tk.mainloop()

main()
