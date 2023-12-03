import sys
# from tkinter import ttk, filedialog, PhotoImage
from tkinter import *
from grabcut_new import GrabCut
from PIL import Image, ImageTk, ImageMath, ImageDraw
import numpy as np

COLOR = {
    'red' : [0, 0, 255],
    'white' : [255, 255, 255],
    'black' : [0, 0, 0],
    'yellow' : "#FFFF00"
}

F_BG = 0
F_FG = 1
F_PR_FG = 2

KOTAK = {
    "coord" : (),
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

# ix, iy, x, y = 176, 47, 351, 189
# print("titik kotak [ix, iy, x, y]: ",[ix, iy, x, y])

class ImageEditing:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Image Segmentation using Grabcut")   
        self.image_path = image_path    

        # Create a frame for canvases
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(side=TOP, fill=X)

        # Create a frame for buttons
        self.button_frame = Frame(self.root)
        self.button_frame.pack(side=BOTTOM, fill=BOTH)

        # Laod image
        self.image = Image.open(self.image_path)

        # Resize ukuran gambar
        self.setSizeImg() 
        self.image = self.image.resize((new_width, new_height)) # <-- untuk resize ukuran

        self.gambar = np.array(self.image)
        self.gambar2 = self.gambar.copy()
        print("ukuran gambar: ", self.gambar.shape)

        # buat masking dari gambar awal
        self.mask = np.zeros(self.gambar2.shape[:2], dtype=np.uint8)
        self.mask2 = self.mask.copy()

        
        self.LoadCanvas()

        # Display canvas
        self.main_canvas.pack(side=LEFT)
        self.mask_canvas.pack(side=LEFT)
        self.result_canvas.pack(side=LEFT)

        # Display Buttons
        self.draw_rect_button.pack()
        self.draw_brush_button.pack()
        self.segmentation_button.pack()
        self.reset_button.pack()


    def LoadCanvas(self):    

        # Make image as main canvas
        self.photo = ImageTk.PhotoImage(self.image)
        self.main_canvas = Canvas(self.canvas_frame, width=self.image.width, height=self.image.height)
        self.main_canvas.create_image(0, 0, anchor=NW, image=self.photo)

        # Create mask canvas
        self.mask_image = Image.fromarray(self.mask)
        self.mask_image = self.mask_image.resize((new_width, new_height)) # <-- untuk resize ukuran
        self.mask_photo = ImageTk.PhotoImage(self.mask_image)
        self.mask_canvas = Canvas(self.canvas_frame, width=self.image.width, height=self.image.height)
        self.mask_canvas.create_image(0, 0, anchor=NW, image=self.mask_photo)

        # Create a result canvas for result display
        self.result_image = Image.new("RGB", (self.image.width, self.image.height))
        self.result_photo = ImageTk.PhotoImage(self.result_image)
        self.result_canvas = Canvas(self.canvas_frame, width=self.image.width, height=self.image.height)
        self.result_canvas.create_image(0, 0, anchor=NW, image=self.result_photo)

        # Create the buttons and add them to the frame
        self.draw_rect_button = Button(self.button_frame, text="Draw Rectangle", command=self.drawing_rectangle)
        self.draw_brush_button = Button(self.button_frame, text="Draw Brush", command=self.drawing_brush)
        self.segmentation_button = Button(self.button_frame, text="Segmentation Grabcut", command=self.segmentation_image)
        self.reset_button = Button(self.button_frame, text="Reset", command=self.reset_image)

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
        print("Keberadaan kotak: ",KOTAK["is_drawn"])
        if KOTAK["is_drawn"] is not True:
            KOTAK["titik_start"] = (event.x, event.y)
        else:
            print("kotak sudah ada")


    def onDrag_rect(self, event):
        if KOTAK["is_drawn"] is not True:
            KOTAK["titik_akhir"] = (event.x, event.y)
            self.update_image()
        # else:
        #     print("kotak sudah ada")
        # if KOTAK["pos"]:
        #     self.main_canvas.delete(KOTAK["pos"])
        # x, y = KOTAK["titik_start"]
        # KOTAK["pos"] = self.main_canvas.create_rectangle(x, y, event.x, event.y, outline=COLOR["yellow"], width=2)

    def onRelease_rect(self, event):
        if KOTAK["titik_start"] and KOTAK["titik_akhir"]:
            KOTAK["coord"] = (self.get_rectangle_coords())
            print("Koordinat Kotak: ", KOTAK["coord"])
            KOTAK["titik_start"] = None
            KOTAK["titik_akhir"] = None
            KOTAK["is_drawn"] = True
        print("Keberadaan kotak: ",KOTAK["is_drawn"])
        print("Koordinat Kotak: ", KOTAK["coord"])


    def update_image(self):
        # Update the main canvas with image and annotations
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((new_width, new_height))  # <-- untuk resize ukuran
        self.draw = ImageDraw.Draw(self.image)
        for coords in KOTAK["coord"]:
            self.draw.rectangle(coords, outline="yellow", width=2)
        self.draw.rectangle(self.get_rectangle_coords(), outline="yellow", width=2)
        self.photo = ImageTk.PhotoImage(self.image)
        self.main_canvas.create_image(0, 0, anchor=NW, image=self.photo)
    
    def update_result(self):
        # Update mask canvas with segmentation
        self.mask_image = Image.fromarray(self.mask)
        self.mask_image = self.mask_image.resize((new_width, new_height)) # <-- untuk resize ukuran
        self.mask_photo = ImageTk.PhotoImage(self.mask_image)
        self.mask_canvas.create_image(0, 0, anchor=NW, image=self.mask_photo)

        # Update image with segmentation
        self.result_image = Image.composite(self.image, Image.new("RGB", self.image.size, "black"), self.mask_image)
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
        gc = GrabCut(self.gambar2, self.mask2, KOTAK["coord"])
        self.mask = np.where((self.mask2 == F_FG) | (self.mask2 == F_PR_FG), 255, 0).astype('uint8')
        self.update_result()

    def reset_image(self):
        # Reset relevant variables
        KOTAK["coord"] = ()
        KOTAK["is_drawn"] = False
        KOTAK["titik_start"] = None
        KOTAK["titik_akhir"] = None
       
        # Laod image
        self.image = Image.open(self.image_path)

        # Resize ukuran gambar
        self.setSizeImg() 
        self.image = self.image.resize((new_width, new_height)) # <-- untuk resize ukuran

        self.gambar = np.array(self.image)
        self.gambar2 = self.gambar.copy()
        print("ukuran gambar: ", self.gambar.shape)

        # buat masking dari gambar awal
        self.mask = np.zeros(self.gambar2.shape[:2], dtype=np.uint8)
        self.mask2 = self.mask.copy()
        
        self.LoadCanvas()