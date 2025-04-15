# Select Video
# load video
# Play video
# Select object id model
# trigger frame detect on frames


import cv2
import tkinter as tk
from PIL import Image, ImageTk
import imageio.v3 as iio
import threading
import time

app = {
        "title": "Person Detector",
        "video_player_width": 500
        }

def image_cv_to_tk(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    photo = ImageTk.PhotoImage(Image.fromarray(img_rgb))
    return photo

def cv_image_scale(cvimage,new_width=200):
    aspect_ratio = new_width / cvimage.shape[1] 
    new_height = int(cvimage.shape[0] * aspect_ratio) 
    scaled_image = cv2.resize(cvimage,(new_width,new_height),interpolation=cv2.INTER_LANCZOS4)
    return scaled_image

class VideoPlayer:
    def __init__(self, parent, video_path):
        # video playing properties
        self.quit = False
        self.play = False
        self.current_frame_idx = 0

        self.parent = parent # root frame

        # video displaying properties
        self.video_path = video_path
        self.video_reader = iio.imiter(video_path)
        self.video_meta = iio.immeta(video_path)
        self.video_label = tk.Label(self.parent)
        self.video_label.pack()

        # debug label
        self.debug_label = tk.Label(self.parent)
        self.debug_label.pack()

        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()

    def update(self):
        global app
        debug_text = ""
        frames =  []
        fps = self.video_meta["fps"]

        for i, frame in enumerate(self.video_reader):
            frame = cv_image_scale(frame,app['video_player_width'])
            frame = image_cv_to_tk(frame)
            frames.append(frame) 

        while not self.quit:
            debug_text = ""
            if self.play:
                    self.current_frame_idx += 1 
            self.current_frame_idx %= len(frames)
            self.video_label.config(image=frames[self.current_frame_idx])
            time.sleep(1/fps)
            debug_text = f"current frame: {self.current_frame_idx}\n"
            self.debug_label.config(text=debug_text)

    def stop(self):
        self.thread.join()

 
def set_up_buttons():
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

def main():
    global app
    video_path = "video/maplocation.mp4"
    root = tk.Tk()
    app['root'] = root
    root.title(app['title'])

    video_player = VideoPlayer(root,video_path)
    app['video_player'] = video_player

    set_up_buttons()

    # root.protocol("WM_DELETE_WINDOW",lambda : video_player.stop())
    root.mainloop()


main()
