import sys
import os
# from tkinter import ttk, filedialog, PhotoImage
from tkinter import *
from grabcut import GrabCut
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
    def __init__(self, root, image_path, image_name, category):
        self.root = root
        self.root.title("Image Segmentation using Grabcut")   
        self.image_path = image_path    
        self.image_name = image_name
        self.category = category

        # Create a frame for title labels
        self.title_frame = Frame(self.root)
        self.title_frame.pack(side=TOP, fill=X)

        # Create a frame for canvases
        self.canvas_frame = Frame(self.root)
        self.canvas_frame.pack(side=TOP, fill=BOTH, expand=YES)  # Adjusted to fill both X and Y, expand

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




    def LoadCanvas(self):    

        # Make image as main canvas
        main_title_label = Label(self.title_frame, text="Main Canvas", font=('Helvetica', 10, 'bold'))
        self.photo = ImageTk.PhotoImage(self.image)
        self.main_canvas = Canvas(self.canvas_frame, width=self.image.width, height=self.image.height)
        self.main_canvas.create_image(0, 0, anchor=NW, image=self.photo)

        # Create mask canvas
        mask_title_label = Label(self.title_frame, text="Mask Canvas", font=('Helvetica', 10, 'bold'))
        self.mask_image = Image.fromarray(self.mask)
        self.mask_image = self.mask_image.resize((new_width, new_height)) # <-- untuk resize ukuran
        self.mask_photo = ImageTk.PhotoImage(self.mask_image)
        self.mask_canvas = Canvas(self.canvas_frame, width=self.image.width, height=self.image.height)
        self.mask_canvas.create_image(0, 0, anchor=NW, image=self.mask_photo)

        # Create a result canvas for result display
        result_title_label = Label(self.title_frame, text="Result Canvas", font=('Helvetica', 10, 'bold'))
        self.result_image = Image.new("RGB", (self.image.width, self.image.height))
        self.result_photo = ImageTk.PhotoImage(self.result_image)
        self.result_canvas = Canvas(self.canvas_frame, width=self.image.width, height=self.image.height)
        self.result_canvas.create_image(0, 0, anchor=NW, image=self.result_photo)

        
        # Create the buttons with custom styles
        self.draw_rect_button = Button(self.button_frame, text="Draw Rectangle", command=self.drawing_rectangle, bg='#4CAF50', fg='white', font=('Helvetica', 10))
        self.segmentation_button = Button(self.button_frame, text="Segmentation Grabcut", command=self.segmentation_image, bg='#2196F3', fg='white', font=('Helvetica', 10))
        self.save_button = Button(self.button_frame, text="Save Result", command=self.save_result_image, bg='#FFC107', fg='black', font=('Helvetica', 10))
        self.reset_button = Button(self.button_frame, text="Restart Program", command=self.reset_image, bg='#607D8B', fg='white', font=('Helvetica', 10))
        
        # Display canvas
        self.main_canvas.pack(side=LEFT)
        main_title_label.pack(side=LEFT, padx=(10, 220))

        # self.mask_canvas.pack(side=LEFT)
        # mask_title_label.pack(side=LEFT, padx=(10, 220))

        self.result_canvas.pack(side=LEFT)
        result_title_label.pack(side=LEFT, padx=(10, 220))

        # Display Buttons
        self.draw_rect_button.pack(side=LEFT, expand=YES, fill=BOTH, padx=5, pady=(10, 10))
        self.segmentation_button.pack(side=LEFT, expand=YES, fill=BOTH, padx=5, pady=(10, 10))
        self.save_button.pack(side=LEFT, expand=YES, fill=BOTH, padx=5, pady=(10, 10))        
        self.reset_button.pack(side=LEFT, expand=YES, fill=BOTH, padx=5, pady=(10, 10))

    def setSizeImg(self):
        global new_width, aspect_ratio, new_height
        # set ukuran gambar
        new_width = 320  # Atur ukuran hanya 480 px
        aspect_ratio = self.image.width / self.image.height
        new_height = int(new_width / aspect_ratio)

    def drawing_brush(self):
        print("mulai gambar brush")

    def drawing_rectangle(self):
        print("mulai gambar kotak")
        self.main_canvas.bind("<ButtonPress-1>", self.onClick_rect)
        self.main_canvas.bind("<B1-Motion>", self.onDrag_rect)
        self.main_canvas.bind("<ButtonRelease-1>", self.onRelease_rect)

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
        self.image2 = self.image.copy()
        self.draw = ImageDraw.Draw(self.image)
        for coords in KOTAK["coord"]:
            self.draw.rectangle(coords, outline="yellow", width=2)
        self.draw.rectangle(self.get_rectangle_coords(), outline="yellow", width=2)
        self.photo = ImageTk.PhotoImage(self.image)
        self.main_canvas.create_image(0, 0, anchor=NW, image=self.photo)
    
    def update_result(self):
        # Update main image with rect
        # self.image_with_rect = Image.fromarray(self.photo)


        # Update mask canvas with segmentation
        self.mask_image = Image.fromarray(self.mask)
        self.mask_image = self.mask_image.resize((new_width, new_height)) # <-- untuk resize ukuran
        self.mask_photo = ImageTk.PhotoImage(self.mask_image)
        self.mask_canvas.create_image(0, 0, anchor=NW, image=self.mask_photo)

        # Update image with segmentation
        self.result_image = Image.composite(self.image2, Image.new("RGB", self.image.size, "black"), self.mask_image)
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


    def save_result_image(self):
        save_folder = f"results/{self.category}"

        # Create the folder if it doesn't exist
        os.makedirs(save_folder, exist_ok=True)

        result_filename = f"result_{self.image_name}.jpg"
        main_rect_filename = f"image_{self.image_name}_rect.jpg"

        self.result_image.save(os.path.join(save_folder, result_filename))
        self.image.save(os.path.join(save_folder, main_rect_filename))

        print("Result image saved successfully:")

    def reset_image(self):
        # Reset image and mask to initial state
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((new_width, new_height))  # <-- untuk resize ukuran
        self.gambar = np.array(self.image)
        self.gambar2 = self.gambar.copy()
        self.mask = np.zeros(self.gambar2.shape[:2], dtype=np.uint8)
        self.mask2 = self.mask.copy()

        # Reset annotation variables
        KOTAK["coord"] = ()
        KOTAK["is_init"] = False
        KOTAK["is_drawn"] = False

        # Reload main canvas
        self.photo = ImageTk.PhotoImage(self.image)
        self.main_canvas.create_image(0, 0, anchor=NW, image=self.photo)

        # Clear the mask canvas
        self.mask_image = Image.fromarray(self.mask)
        self.mask_image = self.mask_image.resize((new_width, new_height)) # <-- untuk resize ukuran
        self.mask_photo = ImageTk.PhotoImage(self.mask_image)
        self.mask_canvas.create_image(0, 0, anchor=NW, image=self.mask_photo)

        # Clear the result canvas
        self.result_image = Image.new("RGB", (self.image.width, self.image.height))
        self.result_photo = ImageTk.PhotoImage(self.result_image)
        self.result_canvas.create_image(0, 0, anchor=NW, image=self.result_photo)
