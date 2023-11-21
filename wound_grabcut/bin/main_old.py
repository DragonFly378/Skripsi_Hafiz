# import sys
# import numpy as np
# import cv2 as cv

# COLOR = {
#     'red' : [0, 0, 255],
#     'white' : [255, 255, 255],
#     'black' : [0, 0, 0],
#     'yellow' : [0, 255, 255]
# }

# kotak = {
#     "size" : (0,0,0,0),
#     'is_init' : False,
#     'is_draw' : False,
# }

# ix, iy, x, y = 176, 47, 351, 189
# # ix, iy, x, y = 0,0,0,0

# def mouseHandler(event, x, y, flags, param):
#     global img, img_copy, mask_img, kotak, ix, iy
    
#     # Gambar kotak
#     if event == cv.EVENT_RBUTTONDOWN:
#         kotak['is_init'] = True
#         ix = x
#         iy = y

#     elif event == cv.EVENT_MOUSEMOVE:
#         if kotak['is_init'] == True:
#             img = img_clone.copy()
#             cv.rectangle(img, (ix, iy), (x, y), COLOR["yellow"], 2)
#             kotak['size'] = (min(ix, x), min(iy, y), abs(ix-x), abs(iy-y))

#     elif event == cv.EVENT_RBUTTONUP:
#         kotak["is_init"] = False
#         kotak["is_draw"] = True
#         cv.rectangle(img, (ix, iy), (x, y), COLOR["yellow"], 2)
#         # img[iy:y, ix:x] = 0 
#         print("titik kotak [ix, iy, x, y]: ",[ix, iy, x, y])
#         mask_img[iy:y, ix:x] = 1




# if __name__ == '__main__':
#     filename = "2.jpg"

#     img = cv.imread(filename)
#     print(img.shape)

#     img_clone = img.copy()
#     mask_img = np.zeros(img.shape[:2], dtype=np.uint8)
#     output = np.zeros(img.shape, np.uint8)           # output image to be shown


#     # input output tampilan gambar
#     cv.namedWindow('hasil')
#     cv.namedWindow('input')
#     cv.moveWindow('input', img.shape[1]+10, 90)
#     cv.setMouseCallback('input', mouseHandler)


#     mask_img[iy:y, ix:x] = 1

#     while(1):
#         cv.imshow('input', img)
#         cv.imshow('hasil', output)
#         key = cv.waitKey(1)



#         mask_res = np.where((mask_img == 1) + (mask_img == 3), 255, 0).astype('uint8')
#         output = cv.bitwise_and(img_clone, img_clone, mask=mask_res)


from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class AnnotationTool:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Annotation Tool")

        # Load the image
        self.image = Image.open(image_path)
        # self.draw = ImageDraw.Draw(self.image)
        self.photo = ImageTk.PhotoImage(self.image)

        # Create the main canvas for image and annotations
        self.main_canvas = Canvas(root, width=self.image.width, height=self.image.height)
        self.main_canvas.pack()
        self.main_canvas.create_image(0, 0, anchor=NW, image=self.photo)

        # Create a secondary canvas for result display
        self.result_canvas = Canvas(root, width=self.image.width, height=self.image.height)
        self.result_canvas.pack()
        self.result_image = Image.new("RGB", (self.image.width, self.image.height))
        self.result_photo = ImageTk.PhotoImage(self.result_image)
        self.result_canvas.create_image(0, 0, anchor=NW, image=self.result_photo)

        # Initialize drawing variables
        self.rect_start = None
        self.rect_end = None
        self.rectangles = []

        # Bind events
        self.main_canvas.bind("<Button-1>", self.on_click)
        self.main_canvas.bind("<ButtonRelease-1>", self.on_release)
        self.main_canvas.bind("<B1-Motion>", self.on_drag)

    def on_click(self, event):
        self.rect_start = (event.x, event.y)

    def on_drag(self, event):
        self.rect_end = (event.x, event.y)
        self.update_image()

    def on_release(self, event):
        if self.rect_start and self.rect_end:
            self.rectangles.append(self.get_rectangle_coords())
            print("Rectangle coordinates:", self.rectangles[-1])
            self.rect_start = None
            self.rect_end = None

    def update_image(self):
        # Update the main canvas with image and annotations
        self.image = Image.open(image_path)
        self.draw = ImageDraw.Draw(self.image)
        for coords in self.rectangles:
            self.draw.rectangle(coords, outline="yellow", width=2)
        self.draw.rectangle(self.get_rectangle_coords(), outline="yellow", width=2)
        self.photo = ImageTk.PhotoImage(self.image)
        self.main_canvas.create_image(0, 0, anchor=NW, image=self.photo)

        # Update the result canvas with annotations
        self.result_image = Image.new("RGB", (self.image.width, self.image.height))
        result_draw = ImageDraw.Draw(self.result_image)
        for coords in self.rectangles:
            result_draw.rectangle(coords, outline="yellow", width=2)
        self.result_photo = ImageTk.PhotoImage(self.result_image)
        self.result_canvas.create_image(0, 0, anchor=NW, image=self.result_photo)

    def get_rectangle_coords(self):
        if self.rect_start and self.rect_end:
            x1, y1 = self.rect_start
            x2, y2 = self.rect_end
            return (x1, y1, x2, y2)
        else:
            return None

    def save_image(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            self.image.save(output_path, "PNG")

if __name__ == "__main__":
    root = Tk()
    image_path = "2.jpg"  # Replace with the path to your image
    tool = AnnotationTool(root, image_path)

    menu = Menu(root)
    root.config(menu=menu)
    file_menu = Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save", command=tool.save_image)
    file_menu.add_command(label="Exit", command=root.quit)

    root.mainloop()
