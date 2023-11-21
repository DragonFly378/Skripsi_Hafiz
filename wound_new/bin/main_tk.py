import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

class RectangleDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Rectangle and Circle Drawing")
        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.rect_start = None
        self.rect = None
        self.image = None
        self.image_path = None

        open_button = tk.Button(root, text="Open Image", command=self.open_image)
        open_button.pack()

        self.drawing_rect = False
        self.drawing_circle = False
        self.rect_coords = None
        self.circle_coords = []

        draw_rect_button = tk.Button(root, text="Draw Rectangle", command=self.start_drawing_rectangle)
        draw_rect_button.pack()

        draw_circle_button = tk.Button(root, text="Draw Circle", command=self.start_drawing_circle)
        draw_circle_button.pack()

    def open_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.ppm")])
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

    def start_drawing_rectangle(self):
        self.drawing_rect = True
        self.canvas.bind("<ButtonPress-3>", self.start_rectangle)
        self.canvas.bind("<B3-Motion>", self.update_rectangle)
        self.canvas.bind("<ButtonRelease-3>", self.finish_rectangle)

    def start_rectangle(self, event):
        self.rect_start = (event.x, event.y)

    def update_rectangle(self, event):
        print(self.rect)
        if self.rect:
            self.canvas.delete(self.rect)
        x, y = self.rect_start
        self.rect = self.canvas.create_rectangle(x, y, event.x, event.y, outline="blue", width=2)

    def finish_rectangle(self, event):
        x1, y1, x2, y2 = self.rect_start[0], self.rect_start[1], event.x, event.y
        self.rect_coords = (x1, y1, x2, y2)
        self.canvas.delete(self.rect)
        self.rect = None
        self.drawing_rect = False

    def start_drawing_circle(self):
        self.drawing_circle = True
        self.canvas.bind("<Button-1>", self.draw_circle)

    def draw_circle(self, event):
        if self.rect_coords is not None:
            x, y = event.x, event.y
            if (self.rect_coords[0] <= x <= self.rect_coords[2]) and (self.rect_coords[1] <= y <= self.rect_coords[3]):
                self.circle_coords.append((x, y))
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, outline="red", width=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = RectangleDrawer(root)
    root.mainloop()
