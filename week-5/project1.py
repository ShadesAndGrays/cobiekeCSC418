# Select Video
# --load video
# --Play video
# Select object id model
# trigger frame detect on frames


from sys import is_stack_trampoline_active
import cv2
import tkinter as tk
import tkinter.filedialog as fd
from PIL import Image, ImageTk
import imageio.v3 as iio
import threading
import time
import numpy as np
import os

app = {
        "title": "Person Detector",
        "video_player_compressed_width": 200,
        "video_player_width": 500
        }


### YOLO 
net = cv2.dnn.readNet('cfg/yolov3.weights','cfg/yolov3.cfg')
classes = []

with open('cfg/coco.names', 'r') as f:
    classes = f.read().splitlines()
###

class ImageFilter:

    @staticmethod
    def cv_image_scale(cvimage,radius=200):
        if cvimage.shape[1] > cvimage.shape[0]:
            aspect_ratio = radius / cvimage.shape[1] 
            new_height = int(cvimage.shape[0] * aspect_ratio) 
            scaled_image = cv2.resize(cvimage,(radius,new_height),interpolation=cv2.INTER_LANCZOS4)
        else:
            aspect_ratio = radius / cvimage.shape[0] 
            new_width = int(cvimage.shape[1] * aspect_ratio) 
            scaled_image = cv2.resize(cvimage,(new_width,radius),interpolation=cv2.INTER_LANCZOS4)
        return scaled_image

    @staticmethod
    def detect_face_haar(image):
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image,scaleFactor=1.3,minNeighbors=5,minSize=(10,30))
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y), (x+w,y+h),(0,255,0),2)
        return image
    @staticmethod
    def detect_object_yolo(image):
        height,width , _ = image.shape

        blob = cv2.dnn.blobFromImage(image,1/255.0,(416,416),swapRB=True,crop=False)
        net.setInput(blob)

        output_layers_names = net.getUnconnectedOutLayersNames()
        layer_outputs = net.forward(output_layers_names)

        boxes = []
        confidences = []
        class_ids = []

        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x,y,w,h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0,255,size=(len(classes),3))

        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = colors[i]
            cv2.rectangle(image,(x,y),(x+w,y+h),color,2)
            cv2.putText(image,label + " " + confidence, (x,y+20),font,2,(255,255,255),2)
        return image



def image_cv_to_tk(image):
    # img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(Image.fromarray(image))
    return photo


class VideoPlayer:

    def select_file(self):
        file = fd.askopenfilename()
        self.load(file)

    def __init__(self):
        global app
        # video playing properties
        self.quit = False
        self.play = False
        self.current_frame_idx = 0
        self.parent = tk.Frame(app['root'],width=app['video_player_width'] * 2)
        self.parent.pack(expand=True)

        self.video_label = tk.Label(self.parent)
        self.video_label.grid(row=0,column=0,columnspan=5)

        # debug label
        self.debug_label = tk.Label(self.parent)
        self.debug_label.grid(row=1,column=0)

        # video
        self.video_path = ""
        self.frames =  []

        # video
        self.update_thread = threading.Thread(target=self.update, args=())
        self.update_thread.daemon = True
        self.update_thread.start()
        self.load_thread = threading.Thread(target=self.load_frames, args=())
        self.load_thread.daemon = True
        self.loading = False
        self.can_load = True
        self.load_thread.start()

    def load(self, video_path):
        if not self.can_load:
            self.loading = False
            return

        # video displaying properties
        self.play = False
        self.frames = []
        self.current_frame_idx = 0
        self.video_label.config(text=f'Loading {video_path}...',background='black',image="",foreground='white')

        self.video_path = video_path
        self.video_reader = iio.imiter(video_path)
        self.video_meta = iio.immeta(video_path)
        self.fps = self.video_meta["fps"]
        self.loading = True

    def load_frames(self):
        while True:
            if self.loading:
                    self.can_load = False
                    filter = ImageFilter.detect_object_yolo
                    for i, frame in enumerate(self.video_reader):
                        if self.quit or not self.loading:
                            break
                        try:
                            frame = filter(frame)
                        except:
                            print("failed to apply filter to frame",i)
                        frame = ImageFilter.cv_image_scale(frame,app['video_player_width'])
                        frame = image_cv_to_tk(frame)
                        self.frames.append(frame) 
                    self.loading = False
                    self.can_load = True
                    pass
            else:
                time.sleep(1)

    def update(self):
        global app
        debug_text = ""

        print(" Update thread started")
        while True:
            debug_text = ""
            if self.loading:
                debug_text += f"Loading {len(self.frames)}/{round(self.video_meta['fps'] *  self.video_meta['duration'])}\n"
            else:
                debug_text += "Loaded\n"
            debug_text += f"video name: {self.video_path}\n"

            if not self.quit:
                if len(self.frames) <=0:
                    debug_text += f"No video loaded\n"
                    time.sleep(0.5)
                else:
                    if self.play:
                        self.current_frame_idx += 1 
                        self.current_frame_idx %= len(self.frames)
                        self.video_label.config(image=self.frames[self.current_frame_idx])
                    else:
                        self.current_frame_idx %= len(self.frames)
                        self.video_label.config(image=self.frames[self.current_frame_idx])
                    time.sleep(1/self.fps)
                    debug_text += f"current frame: {self.current_frame_idx}\n"
                self.debug_label.config(text=debug_text)
            else:
                print(" Update thread stopped")
                break

    def stop(self):
        print("quiting video")
        self.play = False
        self.loading = False
        self.quit = True
        print("Closing")
 
def set_up_control_buttons():
    global app
    video_player = app['video_player']

    control_panel = tk.Frame(app['root']) 
    app['control_panel'] = control_panel
    control_panel.pack()
    
    def toggle_play():
        video_player.play = not video_player.play
        play_button.config(text=('pause' if video_player.play else 'play'))

    def step(steps):
        video_player.current_frame_idx += steps

    step_b1_button = tk.Button(control_panel,text="<") 
    step_b1_button.bind('<Button-1>',lambda e : step(-1))
    step_b1_button.grid(row=0,column=0)
    play_button = tk.Button(control_panel,text="play") 
    play_button.bind('<Button-1>',lambda e : toggle_play())
    play_button.grid(row=0,column=1)
    step_f1_button = tk.Button(control_panel,text=">") 
    step_f1_button.bind('<Button-1>',lambda e : step(+1))
    step_f1_button.grid(row=0,column=2)
    load_button = tk.Button(control_panel,text="Load Video") 
    load_button.bind('<Button-1>',lambda e : app['video_player'].select_file())
    load_button.grid(row=1,column=0,columnspan=3)

def set_up_video_buttons():
    global app
    base_path = "video"
    for i in os.listdir(base_path):
        video_button = tk.Button(text=i)
        video_button.pack()
        video_button.bind('<Button-1>',lambda e ,file=i: app['video_player'].load(f'{base_path}/{file}'))


def main():
    global app
   
    root = tk.Tk()
    app['root'] = root
    root.title(app['title'])
    
    video_player = VideoPlayer()
    app['video_player'] = video_player

    set_up_control_buttons()
    set_up_video_buttons()

    def exit():
        root.destroy()
    root.protocol("WM_DELETE_WINDOW",lambda : exit())
    root.mainloop()


main()
