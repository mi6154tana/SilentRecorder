# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.
import tkinter as tk
from tkinter import ttk
from time import sleep
from PIL import Image, ImageTk
import os

class CreatePage:
    p_frame = None
    p_name = None
    cv = None
    contents = []
    cons_labels = []
    d_positoin = 0

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

        self.contents = self._get_list_cons(p_num)
        if len(self.contents) == 0:
            print('No contents')
        for i in range(len(self.contents)):
            self.contents[i] = self.contents[i].strip(".txt")
            print(self.contents[i])
        for i in range(len(self.contents)):
            if i > 4:
                break #仮
            self.cv.create_polygon(100,90+i*100, 924,90+i*100, 924,170+i*100, 100,170+i*100, fill = 'blue',)

    def _get_list_cons(self, p_num):
        if p_num == 0:
            return ['通常演奏', '正確性診断', '記録', '設定', '終了']
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
    
    def draw_cons(self):
        for i in range(len(self.cons_labels)):
            self.cons_labels[i].place_forget()
        self.cons_labels.clear()

        counter = 0
        for i in range(self.d_positoin, self.d_positoin+5):
            if i > len(self.contents)-1:
                break
            self.cons_labels.append(tk.Label(self.p_frame, text = self.contents[i], foreground = 'white', background = 'blue',font = ("",40,"bold")))
            self.cons_labels[counter].place(x = 100, y = 95 + counter*100)
            counter += 1

    def draw_select(self, c_num):
        c_num -= 1 #都合
        self.cv.delete('select')
        self.cv.create_polygon(90,80+c_num*100, 100,80+c_num*100, 100,180+c_num*100, 90,180+c_num*100, fill = 'red',tag = 'select')
        self.cv.create_polygon(924,80+c_num*100, 934,80+c_num*100, 934,180+c_num*100, 924,180+c_num*100, fill = 'red',tag = 'select')
        self.cv.create_polygon(100,80+c_num*100, 934,80+c_num*100, 934,90+c_num*100, 100,90+c_num*100, fill = 'red',tag = 'select')
        self.cv.create_polygon(100,170+c_num*100, 934,170+c_num*100, 934,180+c_num*100, 100,180+c_num*100, fill = 'red',tag = 'select')
    
    def raise_page(self):
        self.d_positoin = 0   
        self.p_frame.tkraise()
        self.draw_cons()
        self.draw_select(1)