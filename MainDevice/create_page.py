# GUIを扱う
import tkinter as tk
from tkinter import ttk
from time import sleep
from PIL import Image, ImageTk

class CreatePage:
    p_frame = None
    p_name = None
    cv = None
    def __init__(self, root, name, contents):
        self.p_frame = tk.Frame(root)
        self.p_name = name
        #キャンバスを作る
        self.cv = tk.Canvas(self.p_frame,width = 1024, height = 600)
        #self.cv.create_rectangle(0, 0, 800, 450, fill = 'green')#塗りつぶし
        #キャンバスバインド
        self.cv.place(x=0, y=0)
        self.create_cons(root, contents)
        #self.p_frame.pack()
        self.p_frame.grid(row=0, column=0, sticky="nsew")

    def create_cons(self, root, contents):
        name_label_font  = ("Helevetice", 14)
        name_label = ttk.Label(self.p_frame, text = self.p_name, font = name_label_font)
        name_label.grid(row=4, column=0)

        self.cv.create_polygon(10,10, 20,10, 20,20, 10,20, fill = 'red',)
        if len(contents) == 0:
            print('No contents')
        for i in range(len(contents)):
            print(contents[i])
            self.cv.create_polygon(10,10+i*50, 500,10+i*50, 500,50+i*50, 10,50+i*50, fill = 'red',)

    def raise_page(self):     
        self.p_frame.tkraise()