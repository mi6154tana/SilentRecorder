# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.
import tkinter as tk
from tkinter import ttk
from time import sleep
from PIL import Image, ImageTk
import os
from normal_play import NormalPlay

class CreatePage:
    contents = []
    cons_labels = []
    d_positoin = 0

    def __init__(self, root, name, p_num):
        self.p_frame = tk.Frame(root)
        self.p_name = name
        #キャンバスを作る
        self.cv = tk.Canvas(self.p_frame,width = 512, height = 300)
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
            self.cv.create_polygon(50,45+i*50, 462,45+i*50, 462,85+i*50, 50,85+i*50, fill = 'blue',)

    def _get_list_cons(self, p_num):
        if p_num == 0:
            return ['通常演奏', '正確性診断', '記録', '設定', '終了']
        elif p_num == 1:
            return []
        elif p_num == 2 or p_num == 4:
            if p_num == 2:
                path = './Score'
            else:
                path = './Memory'
            files = os.listdir(path)
            files_file = [f for f  in files if os.path.isfile(os.path.join(path, f))]
            return files_file
        elif p_num == 6:
            return ['メトロノーム', '正確性診断中の記録', '演奏デバイスの調整']
        elif p_num == 7:
            return ['電源を切る']
        else:
            return ['None']
    
    def draw_cons(self):
        if self.p_name == 'NORMAL_PLAY':
            norply = NormalPlay(self.cv)
            norply.npmain()
            
        for i in range(len(self.cons_labels)):
            self.cons_labels[i].place_forget()
        self.cons_labels.clear()

        counter = 0
        for i in range(self.d_positoin, self.d_positoin+5):
            if i > len(self.contents)-1:
                break
            #listbox.insert(tk.END,self.contents[i])#tk.Label(self.p_frame, text = self.contents[i], foreground = 'white', background = 'blue',font = ("",20,"bold")))
            self.cons_labels.append(tk.Label(self.p_frame, text = self.contents[i], foreground = 'white', background = 'blue',font = ("",20,"bold")))
            self.cons_labels[counter].place(x = 50, y = 47 + counter*50)
            counter += 1
        
        #scrollbarの処理
        scrollbar = tk.Scrollbar(self.p_frame)
        scrollbar.place(relx = 0.9,relheight=1.0)
        scroll_unit = 1/(1+abs(5-len(self.contents))) 
        #print("contents:",scroll_unit)
        #print([scroll_unit*self.d_positoin,scroll_unit+scroll_unit*self.d_positoin])
        if len(self.contents) > 5:
             scrollbar.set(scroll_unit*self.d_positoin,scroll_unit+scroll_unit*self.d_positoin)
        else:
            scrollbar.set(0,1.0)

    def draw_select(self, c_num):
        c_num -= 1 #都合
        self.cv.delete('select')
        self.cv.create_polygon(45,40+c_num*50, 50,40+c_num*50, 50,90+c_num*50, 45,90+c_num*50, fill = 'red',tag = 'select')
        self.cv.create_polygon(462,40+c_num*50, 467,40+c_num*50, 467,90+c_num*50, 462,90+c_num*50, fill = 'red',tag = 'select')
        self.cv.create_polygon(50,40+c_num*50, 467,40+c_num*50, 467,45+c_num*50, 50,45+c_num*50, fill = 'red',tag = 'select')
        self.cv.create_polygon(50,85+c_num*50, 467,85+c_num*50, 467,90+c_num*50, 50,90+c_num*50, fill = 'red',tag = 'select')
    
    def raise_page(self):
        self.d_positoin = 0   
        self.p_frame.tkraise()
        self.draw_cons()
        print(self.p_name)
        if self.p_name != 'NORMAL_PLAY':
            self.draw_select(1)