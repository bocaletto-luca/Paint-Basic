# Nome del software: Paint Free
# Autore: Luca Bocaletto
# Sito Web: https://www.elektronoide.it
# Licenza: GPLv3

import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog, simpledialog
from PIL import Image, ImageDraw, ImageTk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Free")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.pen_color = "black"
        self.pen_size = 2
        self.drawing = False
        self.last_x, self.last_y = None, None

        # Contenitore per i pulsanti in alto
        self.button_container = tk.Frame(root)
        self.button_container.pack(side=tk.TOP, fill=tk.X)

        self.button_color = tk.Button(self.button_container, text="Choose Color", command=self.choose_color)
        self.button_color.pack(side=tk.LEFT)

        self.button_pen_size = tk.Scale(self.button_container, label="Pen Size", from_=1, to=10, orient="horizontal")
        self.button_pen_size.pack(side=tk.LEFT)
        self.button_pen_size.set(self.pen_size)
        self.button_pen_size.bind("<Motion>", self.update_pen_size)

        self.button_clear = tk.Button(self.button_container, text="Clear", command=self.clear_canvas)
        self.button_clear.pack(side=tk.LEFT)

        self.button_add_image = tk.Button(self.button_container, text="Add Image", command=self.add_image)
        self.button_add_image.pack(side=tk.LEFT)

        self.button_new_project = tk.Button(self.button_container, text="New Project", command=self.create_new_project)
        self.button_new_project.pack(side=tk.LEFT)

        self.button_save_drawing = tk.Button(self.button_container, text="Save Drawing", command=self.save_drawing)
        self.button_save_drawing.pack(side=tk.LEFT)

        self.active_image = None
        self.draw_on_image = False

    def start_drawing(self, event):
        if not self.draw_on_image:
            x, y = event.x, event.y
            self.drawing = True
            self.last_x, self.last_y = x, y

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            if self.last_x and self.last_y:
                self.canvas.create_line(
                    self.last_x,
                    self.last_y,
                    x,
                    y,
                    fill=self.pen_color,
                    width=self.pen_size
                )
                self.last_x, self.last_y = x, y

    def stop_drawing(self, event):
        self.drawing = False

    def choose_color(self):
        color = askcolor()[1]
        if color:
            self.pen_color = color

    def update_pen_size(self, event):
        self.pen_size = self.button_pen_size.get()

    def clear_canvas(self):
        self.canvas.delete("all")

    def add_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image = Image.open(file_path)
            self.active_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.active_image)
            self.draw_on_image = True

    def create_new_project(self):
        new_width = simpledialog.askinteger("New Project", "Enter width (in pixels):", parent=self.root, minvalue=1)
        new_height = simpledialog.askinteger("New Project", "Enter height (in pixels):", parent=self.root, minvalue=1)
        if new_width and new_height:
            self.canvas.config(width=new_width, height=new_height)

    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas.postscript(file=file_path, colormode="color")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
