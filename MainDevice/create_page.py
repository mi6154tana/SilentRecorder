# GUIを扱う
import tkinter as tk
from tkinter import ttk
from time import sleep
from PIL import Image, ImageTk
import os

class CreatePage:
    p_frame = None
    p_name = None
    cv = None
    def __init__(self, root, name, p_num):
        self.p_frame = tk.Frame(root)
        self.p_name = name
        #キャンバスを作る
        self.cv = tk.Canvas(self.p_frame,width = 1024, height = 600)
        #self.cv.create_rectangle(0, 0, 800, 450, fill = 'green')#塗りつぶし
        #キャンバスバインド
        self.cv.place(x=0, y=0)
        self._create_cons(root, p_num)
        #self.p_frame.pack()
        self.p_frame.grid(row=0, column=0, sticky="nsew")

    def _create_cons(self, root, p_num):
        name_label_font  = ("Helevetice", 14)
        name_label = tk.Label(self.p_frame, text = self.p_name, font = name_label_font)
        name_label.grid(row=4, column=0)
        cons_lavels = []

        contents = self.get_list_cons(p_num)
        if len(contents) == 0:
            print('No contents')
        for i in range(len(contents)):
            print(contents[i])
            self.cv.create_polygon(10,50+i*50, 500,50+i*50, 500,90+i*50, 10,90+i*50, fill = 'blue',)
            cons_lavels.append(tk.Label(self.p_frame, text = contents[i],background = "blue",font = ("",20,"bold")))
            cons_lavels[i].place(x = 10, y = 50+i*50)

    def get_list_cons(self, p_num):
        if p_num == 0:
            return ['通常演奏', '正確性診断', '記録', '設定']
        elif p_num == 2 or p_num == 4:
            if p_num == 2:
                path = './Score'
            else:
                path = './Memory'
            files = os.listdir(path)
            files_file = [f for f  in files if os.path.isfile(os.path.join(path, f))]

            return files_file
        else:
            return ['None']

    def raise_page(self):     
        self.p_frame.tkraise()