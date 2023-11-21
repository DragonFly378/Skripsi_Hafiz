import sys
from tkinter import *
from tkinter import ttk, filedialog
from grabcut import GrabCut
# from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageMath, ImageDraw
import numpy as np

# ix, iy, x, y = 176, 47, 351, 189
# print("titik kotak [ix, iy, x, y]: ",[ix, iy, x, y])



COLOR = {
    'red' : [0, 0, 255],
    'white' : [255, 255, 255],
    'black' : [0, 0, 0],
    'yellow' : "#FFFF00"
}

F_BG = 0
F_FG = 1
F_PR_BG = 2
F_PR_FG = 3

KOTAK = {
    "coord" : [],
    "pos" : None,
    "titik_start" : None,
    "titik_akhir" : None,
    'is_init' : False,
    'is_drawn' : False,
}

BRUSH = {
    "size" : 3,
    'is_init' : False,
    'is_drawn' : False,
}


class ImageEditing:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Image Segmentation using Grabcut")       

        # Create a frame for canvases
        canvas_frame = Frame(root)
        canvas_frame.pack(side=TOP, fill=X)

        # Create a frame for buttons
        button_frame = Frame(root)
        button_frame.pack(side=BOTTOM, fill=BOTH)

        # Laod image
        self.image = Image.open(image_path)
        # self.setSizeImg()
        # self.image = self.image.resize((new_width, new_height))

        self.gambar = np.array(self.image)
        self.gambar2 = self.gambar.copy()
        print("ukuran gambar: ", self.gambar.shape)

        self.gambar = Image.fromarray(self.gambar)

        # make masking from gambar awal
        self.mask = np.zeros(self.gambar2.shape[:2], dtype=np.uint8)
        self.mask2 = self.mask.copy()

        # Make image as main canvas
        self.photo = ImageTk.PhotoImage(self.image)
        self.main_canvas = Canvas(canvas_frame, width=self.image.width, height=self.image.height)
        self.main_canvas.create_image(0, 0, anchor=NW, image=self.photo)

        # Create mask canvas
        self.mask_image = Image.fromarray(self.mask)
        # self.mask_image = self.mask_image.resize((new_width, new_height))
        self.mask_photo = ImageTk.PhotoImage(self.mask_image)
        self.mask_canvas = Canvas(canvas_frame, width=self.image.width, height=self.image.height)
        self.mask_canvas.create_image(0, 0, anchor=NW, image=self.mask_photo)

        # Create a result canvas for result display
        self.result_image = Image.new("RGB", (self.image.width, self.image.height))
        self.result_photo = ImageTk.PhotoImage(self.result_image)
        self.result_canvas = Canvas(canvas_frame, width=self.image.width, height=self.image.height)
        self.result_canvas.create_image(0, 0, anchor=NW, image=self.result_photo)

        # Create the buttons and add them to the frame
        draw_rect_button = Button(button_frame, text="Draw Rectangle", command=self.drawing_rectangle)
        draw_brush_button = Button(button_frame, text="Draw Brush", command=self.drawing_brush)
        segmentation_button = Button(button_frame, text="Segmentation Grabcut", command=self.segmentation_image)
        
        # Display canvas
        self.main_canvas.pack(side=LEFT)
        self.mask_canvas.pack(side=LEFT)
        self.result_canvas.pack(side=LEFT)

        # Display Buttons
        draw_rect_button.pack()
        draw_brush_button.pack()
        segmentation_button.pack()

    def setSizeImg(self):
        global new_width, aspect_ratio, new_height
        # set ukuran gambar
        new_width = 280  # Atur ukuran hanya 480 px
        aspect_ratio = self.image.width / self.image.height
        new_height = int(new_width / aspect_ratio)

    def drawing_brush(self):
        print("mulai gambar brush")

    def drawing_rectangle(self):
        print("mulai gambar kotak")
        self.main_canvas.bind("<ButtonPress-3>", self.onClick_rect)
        self.main_canvas.bind("<B3-Motion>", self.onDrag_rect)
        self.main_canvas.bind("<ButtonRelease-3>", self.onRelease_rect)

    def onClick_rect(self, event):
        KOTAK["titik_start"] = (event.x, event.y)

    def onDrag_rect(self, event):
        KOTAK["titik_akhir"] = (event.x, event.y)
        self.update_image()
        # if KOTAK["pos"]:
        #     self.main_canvas.delete(KOTAK["pos"])
        # x, y = KOTAK["titik_start"]
        # KOTAK["pos"] = self.main_canvas.create_rectangle(x, y, event.x, event.y, outline=COLOR["yellow"], width=2)

    def onRelease_rect(self, event):
        if KOTAK["titik_start"] and KOTAK["titik_akhir"]:
            KOTAK["coord"].append(self.get_rectangle_coords())
            print("Rectangle coordinates:", KOTAK["coord"][-1])
            KOTAK["titik_start"] = None
            KOTAK["titik_akhir"] = None

    def update_image(self):
        # Update the main canvas with image and annotations
        self.image = Image.open(image_path)
        # self.image = self.image.resize((new_width, new_height))
        self.draw = ImageDraw.Draw(self.image)
        for coords in KOTAK["coord"]:
            self.draw.rectangle(coords, outline="yellow", width=2)
        self.draw.rectangle(self.get_rectangle_coords(), outline="yellow", width=2)
        self.photo = ImageTk.PhotoImage(self.image)
        self.main_canvas.create_image(0, 0, anchor=NW, image=self.photo)
    
    def update_result(self):
        # Update mask canvas with segmentation
        self.mask_image = Image.fromarray(self.mask)
        # self.mask_image = self.mask_image.resize((new_width, new_height))
        self.mask_photo = ImageTk.PhotoImage(self.mask_image)
        self.mask_canvas.create_image(0, 0, anchor=NW, image=self.mask_photo)


        # Update the result canvas with annotations
        # self.result_image = Image.new("RGB", (self.image.width, self.image.height))
        # result_draw = ImageDraw.Draw(self.result_image)
        # for coords in KOTAK["coord"]:
        #     result_draw.rectangle(coords, outline="yellow", width=2)
        # self.result_photo = ImageTk.PhotoImage(self.result_image)
        # self.result_canvas.create_image(0, 0, anchor=NW, image=self.result_photo)

        # Update image with segmentation
        self.result_image = Image.composite(self.gambar, Image.new("RGB", self.gambar.size, "black"), self.mask_image)
        # self.result_image = Image.fromarray(self.mask)
        self.result_photo = ImageTk.PhotoImage(self.result_image)
        self.result_canvas.create_image(0, 0, anchor=NW, image=self.result_photo)
   

    def get_rectangle_coords(self):
        if KOTAK["titik_start"] and KOTAK["titik_akhir"]:
            x1, y1 = KOTAK["titik_start"]
            x2, y2 = KOTAK["titik_akhir"]
            return (x1, y1, x2, y2)
        else:
            return None

    def segmentation_image(self):
        gc = GrabCut(self.gambar2, self.mask2, KOTAK["coord"][-1])
        self.mask = np.where((self.mask2 == F_FG) | (self.mask2 == F_PR_FG), 255, 0).astype('uint8')
        self.update_result()



if __name__ == '__main__':
    root = Tk()
    image_path = "2.jpg"
    tools = ImageEditing(root, image_path)

    root.mainloop()