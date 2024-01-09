from tkinter import Tk, Canvas, PhotoImage, Button, Frame
from PIL import Image, ImageTk
import numpy as np
from grabcut import GrabCut

# Constants
DRAW_BG = 0
DRAW_FG = 1
DRAW_PR_FG = 3

class GrabCutGUI:
    def __init__(self, master, filename):
        self.master = master
        self.master.title("GrabCut Interactive Segmentation")
        
        self.filename = filename
        self.image = Image.open(filename)
        self.img_width, self.img_height = self.image.size
        self.gambar = np.array(self.image)
        self.gambar2 = self.gambar.copy()
        self.mask = None  # Add mask attribute

        self.canvas = Canvas(master, width=self.img_width, height=self.img_height)
        self.canvas.pack()

        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo_image)

        self.rect = None
        self.drawing = False
        self.mode = DRAW_FG

        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<B1-Motion>", self.on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_release)

        self.buttons_frame = Frame(master)
        self.buttons_frame.pack()

        self.bg_button = Button(self.buttons_frame, text="Mark Background", command=self.set_bg_mode)
        self.bg_button.pack(side='left')

        self.fg_button = Button(self.buttons_frame, text="Mark Foreground", command=self.set_fg_mode)
        self.fg_button.pack(side='left')

        self.segment_button = Button(self.buttons_frame, text="Segment Image", command=self.segment_image)
        self.segment_button.pack(side='left')

        self.reset_button = Button(self.buttons_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side='left')

        self.result_image = None

    def on_left_click(self, event):
        self.rect = (event.x, event.y)
        self.drawing = True

    def on_left_drag(self, event):
        if self.drawing:
            self.canvas.delete("rect")
            self.canvas.create_rectangle(self.rect[0], self.rect[1], event.x, event.y, outline='blue', tags="rect")

    def on_left_release(self, event):
        if self.drawing:
            self.rect += (event.x, event.y)
            self.drawing = False
            self.mask = np.zeros((self.img_height, self.img_width), dtype=np.uint8)


    def set_bg_mode(self):
        self.mode = DRAW_BG

    def set_fg_mode(self):
        self.mode = DRAW_FG

    def segment_image(self):
        if self.rect:
            print(self.rect)
            # Assuming the GrabCut class is already defined and imported
            gc = GrabCut(self.gambar2, self.mask, self.rect)
            
            # Update the mask based on foreground and probable foreground
            self.mask = np.where((self.mask == DRAW_FG) | (self.mask == DRAW_PR_FG), 255, 0).astype('uint8')

            # Perform GrabCut algorithm
            # gc.run()

            # Get the segmented result
            # segmented_result = gc.get_segmented_image()

            # Convert the segmented result to PhotoImage format
            self.result_image = ImageTk.PhotoImage(Image.fromarray(segmented_result))

            # Display the segmented result on the canvas
            self.canvas.create_image(0, 0, anchor='nw', image=self.result_image)

            # Perform GrabCut algorithm using PIL (you may need to implement this or use an existing library)
            # Update the result_image with the segmented image
            # Display the result_image on the canvas
            pass

    def reset(self):
        self.canvas.delete("rect")
        self.rect = None
        self.drawing = False
        self.mode = DRAW_FG


if __name__ == "__main__":
    root = Tk()
    app = GrabCutGUI(root, "2.jpg")
    root.mainloop()
