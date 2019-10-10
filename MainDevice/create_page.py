# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.
import tkinter as tk
from tkinter import ttk
from time import sleep
from PIL import Image, ImageTk
import os
from normal_play import NormalPlay
from draw_sound_score_mk2 import DrawScore as DS
import json
import codecs
import os

class CreatePage:

    def __init__(self, root, name, p_num):
        self.draw_mag = 1.0 #フルスクリーン時、表示するディスプレイに合わせるため
        self.p_frame = tk.Frame(root)
        self.p_name = name
        self.contents = []
        self.cons_labels = []
        self.d_positoin = 0
        self.my_num = p_num
        self.selected_fname = ''
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
        
        self.cv.delete('cons')
        self.contents.clear()
        self.contents = self._get_list_cons(p_num)
        if len(self.contents) == 0:
            print('No contents')
        for i in range(len(self.contents)):
            self.contents[i] = self.contents[i].strip(".txt")
            print(self.contents[i])
        for i in range(len(self.contents)):
            if i > 4:
                break #仮
            self.cv.create_polygon(50 *self.draw_mag,45+i*50*self.draw_mag, 462*self.draw_mag,45+i*50*self.draw_mag, 462*self.draw_mag,85+i*50*self.draw_mag, 50*self.draw_mag,85+i*50*self.draw_mag, fill = '#8A2BE2', tag = 'cons')

    def _get_list_cons(self, p_num):
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        if p_num == 0:
            return ['通常演奏', '正確性診断', '記録', '設定', '終了']
        elif p_num == 1:
            return []
        elif p_num == 2 or p_num == 4:
            if p_num == 2:
                path = nowDirectoryPath + 'Score'
            else:
                path = nowDirectoryPath + 'Recording'
            files = os.listdir(path)
            files_file = [f for f  in files if os.path.isfile(os.path.join(path, f))]
            if len(files_file) == 0:
                return ['ファイルが存在しません']
            return files_file

        elif p_num == 6: #設定の描画処理
            view_text = []
            select_volumes = ["小","中","大"]
            config_text_list = ["メトロノーム:","正確性診断の記録:","演奏デバイスの調整:","音量:"]
            with codecs.open(nowDirectoryPath + "config.json","r") as config_file:
                config_obj = json.load(config_file)
            for config_value,config_text in zip(config_obj.values(),config_text_list):
                #音量用の処理
                if config_value in ["0","1","2"]:
                    config_value = select_volumes[int(config_value)]
                view_text.append(config_text+config_value)
            #print("view:",view_text)
            return view_text

        elif p_num == 7:
            return ['電源を切る', 'プログラム終了']
        elif p_num == 8:
            return [self.selected_fname + 'を再生', self.selected_fname + 'を消す']
        else:
            return ['None']

    def set_file_name(self, name):
        self.selected_fname = name

    def draw_cons(self):
        if self.p_name == 'NORMAL_PLAY':
            print('Go to NormalPlay!')
            norply = NormalPlay(self.cv, self.p_frame)
            norply.npmain()
            return

        if self.p_name == 'JUDGE_PLAY':
            print("JUDGE PLAY")
            draw_s = DS(self.selected_fname,self.cv,self.p_frame,"JUDGE_PLAY")
            draw_s.dss_main()
            return

        if self.p_name == "PLAY_RECORDING":
            print("Play_recoding")
            draw_s = DS(self.selected_fname,self.cv,self.p_frame,"PLAY_RECORDING")
            draw_s.dss_main()
            return
            
        for i in range(len(self.cons_labels)):
            self.cons_labels[i].place_forget()
        self.cons_labels.clear()

        counter = 0
        #self.contents = self._get_list_cons(p_num)
        for i in range(self.d_positoin, self.d_positoin+5):
            if i > len(self.contents)-1:
                break
            #listbox.insert(tk.END,self.contents[i])#tk.Label(self.p_frame, text = self.contents[i], foreground = 'white', background = 'blue',font = ("",20,"bold")))
            self.cons_labels.append(tk.Label(self.p_frame, text = self.contents[i], foreground = 'white', background = '#8A2BE2',font = ("",15,"bold")))
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
        self.cv.create_polygon(45*self.draw_mag, 40+c_num*50*self.draw_mag, 50*self.draw_mag,40+c_num*50*self.draw_mag,  50*self.draw_mag,90+c_num*50*self.draw_mag,  45*self.draw_mag,90+c_num*50*self.draw_mag, fill = 'red',tag = 'select')
        self.cv.create_polygon(462*self.draw_mag,40+c_num*50*self.draw_mag, 467*self.draw_mag,40+c_num*50*self.draw_mag, 467*self.draw_mag,90+c_num*50*self.draw_mag, 462*self.draw_mag,90+c_num*50*self.draw_mag, fill = 'red',tag = 'select')
        self.cv.create_polygon(50*self.draw_mag, 40+c_num*50*self.draw_mag, 467*self.draw_mag,40+c_num*50*self.draw_mag, 467*self.draw_mag,45+c_num*50*self.draw_mag, 50*self.draw_mag,45+c_num*50*self.draw_mag, fill = 'red',tag = 'select')
        self.cv.create_polygon(50*self.draw_mag, 85+c_num*50*self.draw_mag, 467*self.draw_mag,85+c_num*50*self.draw_mag, 467*self.draw_mag,90+c_num*50*self.draw_mag, 50*self.draw_mag,90+c_num*50*self.draw_mag, fill = 'red',tag = 'select')
    
    def raise_page(self):
        self.d_positoin = 0   
        self.p_frame.tkraise()
        self._create_cons(self.p_frame, self.my_num)
        self.draw_cons()
        print(self.p_name)
        if self.p_name != 'NORMAL_PLAY' and self.p_name != 'PLAY_RECORDING' and self.p_name != 'JUDGE_PLAY':
            self.draw_select(1)
