# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.

#====================================================================================
# ライブラリ
#====================================================================================
# GUIを扱う
import tkinter as tk
from time import sleep
from PIL import Image, ImageTk

class App(object):
        def __init__(self):
            self.right = False
            self.left = False
            self.up = False
            self.down = False

        def keyPressed(self,event):
            print ("HERE")
            if event.keysym == '1':
                self.right = True
                callback(Button_1)
            elif event.keysym == '2':
                self.left = True
            elif event.keysym == '3':
                self.up = True
            elif event.keysym == '4':
                self.down = True

        def keyReleased(self,event):
            if event.keysym == '1':
                self.right = False
            elif event.keysym == '2':
                self.left = False
            elif event.keysym == '3':
                self.up = False
            elif event.keysym == '4':
                self.down = False

        def task(self):
            if self.right:
                print ('1')
                sleep(0.1)
            elif self.left:
                print ('2')
                sleep(0.1)
            elif self.up:
                print ('3')
                sleep(0.1)
            elif self.down:
                print ('4')
                sleep(0.1)
            window.after(20,self.task)

class DrawPage:
    
    ### そのページ用のFrameを生成
    frame = tkinter.Frame(window)

    ### タイトル表示
    #--- ラベル生成
    # 空白
    spaceLabel = [tkinter.Label(frame, text="") for column in range(3)]
    # タイトル
    titleLabelFont  = ("Helevetice", 89, "bold")
    titleLabel = tk.Label(frame, text="Silent Recorder", font=titleLabelFont)

    button =\

    #--- ラベル配置
    # タイトル
    titleLabel.pack()

    def __init__(self, pname, b_num):
        window = tkinter.Tk()
        # ウィンドウタイトルを決定
        window.title("HOME")

        # ウィンドウの大きさを決定
        window.geometry("400x400")
        window.attributes("-fullscreen", True)

        # ウィンドウのグリッドを 1x1 にする
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
         application = App()

        window.bind_all('<Key>', application.keyPressed)
        window.bind_all('<KeyRelease>', application.keyReleased)
        window.after(20,application.task)

            # Canvas Widget を生成して配置
        canvas = tk.Canvas(window)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbar を生成して配置
        bar = tk.Scrollbar(window, orient=tk.VERTICAL)
        bar.grid(row=0, column=0, sticky="nsew")

        # Scrollbarを制御をCanvasに通知する処理を追加
        bar.config(command=canvas.yview)

        # Canvasのスクロール範囲を設定
        canvas.config(scrollregion=(0,0,400,400))

        # Canvasの可動域をScreoobarに通知する処理を追加
        canvas.config(yscrollcommand=bar.set)

    def draw_button(self, b_text, next_page, x, y):
        tk.Button(frame, text = b_text, height = 1, command = lambda : changePage(next_page)
        #---  ボタン配置
        # 空白
        for index in range(2):
            spaceLabel[index].pack()
        # ボタン
        button.pack(fill = 'x', padx = x, pady = y, side = 'top')
        button["fg"] = '#ffffff'
        button["bg"] = '#1496ff'
        button["font"] = ("",64)