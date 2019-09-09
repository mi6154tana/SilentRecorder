# -*- coding: utf-8 -*-

#====================================================================================
# ライブラリ
#====================================================================================
# GUIを扱う
import tkinter
# tkinterよりデザインが良くなる
import tkinter as tk
import tkinter as ttk
from time import sleep
from PIL import Image, ImageTk
#====================================================================================
# 関数定義
#====================================================================================
#------------------------------------------------------------------------------------
# ボタンを押したときの処理
#------------------------------------------------------------------------------------
def changePage(page):
    # クリックされたページを上位層にする
    page.tkraise()
# ウィジェットがクリックされたときのイベントを定義
def callback(event):
    # ボタンの背景色がデフォルト値だったら変更し、
    if event.widget["bg"] == '#1496ff':
        event.widget["bg"] = '#ffffff'
        event.widget["fg"] = '#1496ff'
    # 元に戻す。
    else:
        event.widget["fg"] = '#ffffff'
        event.widget["bg"] = '#1496ff'
#====================================================================================
# 本体関数
#====================================================================================
# main関数を追加し、スコープを切る
def main() ->None:
    # インスタンス生成
    window = tkinter.Tk()

    # ウィンドウタイトルを決定
    window.title("HOME")

    # ウィンドウの大きさを決定
    window.geometry("400x400")
    window.attributes("-fullscreen", True)

    # ウィンドウのグリッドを 1x1 にする
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
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
    

    #-----------------------------------HOME（先頭ページ）---------------------------------
    ### HOMe用のFrameを生成
    HOME = tkinter.Frame(window)

    ### タイトル表示
    #--- ラベル生成
    # 空白
    spaceLabel1 = [tkinter.Label(HOME, text="") for column in range(3)]
    # タイトル
    titleLabelFont  = ("Helevetice", 89, "bold")
    titleLabel      = ttk.Label(HOME, text="Silent Recorder", font=titleLabelFont)

    #--- ラベル配置
    # タイトル
    titleLabel.pack()
    
    

    
    # ---Scrollbar を生成して配置
    #bar = tk.Scrollbar(window, orient=tk.VERTICAL)
    #bar.pack(side=tk.RIGHT, fill=tk.Y)
    #bar.config(command=window.yview)
    
    # ---Canvas Widget を配置
    #window.config(yscrollcommand=bar.set)
    #window.config(scrollregion=(0,0,400,400)) #スクロール範囲
    #window.pack(side=tk.LEFT, fill=tk.BOTH)
    
    ### ボタン表示
    
  
    
    #---  ボタン生成
    Button_1 =\
     ttk.Button(HOME, text="           演奏           ",height = 1, command=lambda : changePage(doPage))
    #---  ボタン配置
    # 空白
    for index in range(2):
        spaceLabel1[index].pack()
    # ボタン
    Button_1.pack(fill = 'x', padx=20,pady=10, side = 'top')
    Button_1["fg"] = '#ffffff'
    Button_1["bg"] = '#1496ff'
    Button_1["font"] = ("",64)

    
    #---  ボタン生成2
    Button_2 = \
    ttk.Button(HOME, text="           正確性診断           ", fg = '#ffffff',bg = '#1496ff',height = 1, command=lambda : changePage(TUREPage))
    #---  ボタン配置
    # 空白
    for index in range(2):
        spaceLabel1[index].pack()
    # ボタン
    Button_2.pack(fill = 'x', padx=20,pady=10, side = 'top')
    Button_2["font"] = ("",64)
    
    #---  ボタン生成3
    Button_3 = \
    ttk.Button(HOME, text="           再生           ", fg = '#ffffff',bg = '#1496ff',height = 1, command=lambda : changePage(playPage))
    #---  ボタン配置
    # 空白
    for index in range(2):
        spaceLabel1[index].pack()
    # ボタン
    Button_3.pack(fill = 'x', padx=20,pady=10, side = 'top')
    Button_3["font"] = ("",64)
    
    
    
    
    #---  ボタン生成4
    Button_4 = \
    ttk.Button(HOME, text="           メトロノーム           ", fg = '#ffffff',bg = '#1496ff',height = 1, command=lambda : changePage(MtroPage))
    #---  ボタン配置
    # 空白
    for index in range(2):
        spaceLabel1[index].pack()
    # ボタン
    Button_4.pack(fill = 'x', padx=20,pady=10, side = 'top')
    Button_4["font"] = ("",64)
    
    
    
    #HOMEを配置
    HOME.grid(row=0, column=0, sticky="nsew")

    #-----------------------------------doPage（演奏）---------------------------------
    ### doPage用のFrameを生成
    doPage = tkinter.Frame(window)

    ###  空白
    #---  ラベル生成
    spaceLabel1 = [tkinter.Label(doPage, text="") for column in range(5)]
    # タイトル
    titleLabelFont  = ("Helevetice", 32, "bold")
    titleLabel =\
        ttk.Label(doPage, text="Silent Recorder", font=titleLabelFont)
    #---  ラベル配置
    # タイトル
    titleLabel.pack()

    ### フレーム表示
    #---  フレーム生成
    frame = ttk.Frame(doPage)
    #---  フレーム配置
    frame.pack()
    
    spaceLabel2 = [tkinter.Label(frame, text="Do you want to record your performances?") ]
    #--- ラベル配置
    # 空白
    for index in range(1):
        spaceLabel2[index].grid(row=index, column=0)
    
    spaceLabel3 = [tkinter.Label(frame, text="") for column in range(3)]

    #--- ラベル配置
    # 空白
    for index in range(3):
        spaceLabel3[index].grid(row=index, column=0)        
    #--- ボタン生成
    Button =\
     ttk.Button(doPage, text="           Yes I do           ")

    #---  ボタン配置
    # 空白
    # ボタン
    Button.pack(fill = 'x' ,padx=30,side='top')
    
    #--- ボタン生成2
    Button =\
     ttk.Button(doPage, text="           No Performance start           ", command=lambda : changePage(PeSt))

    #---  ボタン配置
    # 空白
    # ボタン
    Button.pack(fill = 'x' ,padx=30,side='top')
    
    #--- ボタン生成3
    Button =\
     ttk.Button(doPage, text="           modoru by do           ", command=lambda : changePage(HOME))

    #---  ボタン配置
    # 空白
    # ボタン
    Button.pack(fill = 'x' ,padx=30,side='top')

    # doPageを配置
    doPage.grid(row=0, column=0, sticky="nsew")
    
 #-----------------------------------TUREPage（正確性）---------------------------------
    ### TUREPage用のFrameを生成
    TUREPage = tkinter.Frame(window)
    
    ###  空白
    #---  ラベル生成
    spaceLabel1 = [tkinter.Label(TUREPage, text="") for column in range(5)]
    # タイトル
    titleLabelFont  = ("Helevetice", 32, "bold")
    titleLabel =\
        ttk.Label(TUREPage, text="Silent Recorder", font=titleLabelFont)
    #---  ラベル配置
    # タイトル
    titleLabel.pack()

    #---  ラベル配置
    # 空白
    for index in range(5):
        spaceLabel1[index].pack()
    # タイトル
    #titleLabel.pack()

    ### フレーム表示
    #---  フレーム生成
    frame = ttk.Frame(TUREPage)
    #---  フレーム配置
    frame.pack()

    ### ユーザー名入力表示
    #--- ラベル生成
    # 空白
    spaceLabel2 = [tkinter.Label(frame, text="") for column in range(3)]

    #--- ラベル配置
    # 空白
    for index in range(3):
        spaceLabel2[index].grid(row=index, column=0)

    #---  ボタン生成
    Button =\
     ttk.Button(TUREPage, text="           modoru by TURE          ", command=lambda : changePage(HOME))

    #---  ボタン配置
    # 空白
    # ボタン
    Button.pack(fill = 'x' ,padx=30,side='top')

    # TUREPageを配置
    TUREPage.grid(row=0, column=0, sticky="nsew")
    
        #-----------------------------------playPage（再生）---------------------------------
    ### playPage用のFrameを生成
    playPage = tkinter.Frame(window)
    
    #---  ラベル生成
    spaceLabel1 = [tkinter.Label(playPage, text="") for column in range(5)]
    # タイトル
    titleLabelFont  = ("Helevetice", 32, "bold")
    titleLabel =\
        ttk.Label(playPage, text="Silent Recorder", font=titleLabelFont)
    #---  ラベル配置
    # タイトル
    titleLabel.pack()
    ###  空白
    #---  ラベル生成
    spaceLabel1 = [tkinter.Label(playPage, text="") for column in range(5)]

    #---  ラベル配置
    # 空白
    for index in range(5):
        spaceLabel1[index].pack()
    # タイトル
    #titleLabel.pack()

    ### フレーム表示
    #---  フレーム生成
    frame = ttk.Frame(playPage)
    #---  フレーム配置
    frame.pack()

    #--- ラベル生成
    # 空白
    spaceLabel2 = [tkinter.Label(frame, text="") for column in range(3)]

    #--- ラベル配置
    # 空白
    for index in range(3):
        spaceLabel2[index].grid(row=index, column=0)

    Button =\
     ttk.Button(playPage, text="           modoru by play          ", command=lambda : changePage(HOME))

    #---  ボタン配置
    # 空白
    # ボタン
    Button.pack(fill = 'x' ,padx=30,side='top')

    # playPageを配置
    playPage.grid(row=0, column=0, sticky="nsew")
    
    #-----------------------------------MtroPage（メトロノーム）---------------------------------
    ### MtroPage用のFrameを生成
    MtroPage = tkinter.Frame(window)

        ###  空白
    #---  ラベル生成
    spaceLabel1 = [tkinter.Label(MtroPage, text="") for column in range(5)]
    # タイトル
    titleLabelFont  = ("Helevetice", 32, "bold")
    titleLabel =\
        ttk.Label(MtroPage, text="Silent Recorder", font=titleLabelFont)
    #---  ラベル配置
    # タイトル
    titleLabel.pack()
    #---  ラベル生成
    spaceLabel1 = [tkinter.Label(MtroPage, text="") for column in range(5)]
    
    #---  ラベル配置
    # 空白
    for index in range(5):
        spaceLabel1[index].pack()

    ### フレーム表示
    #---  フレーム生成
    frame = ttk.Frame(MtroPage)
        
    spaceLabel2 = [tkinter.Label(frame, text="Do you like metronome?") ]
    #--- ラベル配置
    # 空白
    for index in range(1):
        spaceLabel2[index].grid(row=index, column=0)
    #---  フレーム配置
    frame.pack()

    ### ユーザー名入力表示
    #--- ラベル生成
    # 空白
    spaceLabel2 = [tkinter.Label(frame, text="") for column in range(3)]

    #--- ラベル配置
    # 空白
    for index in range(3):
        spaceLabel2[index].grid(row=index, column=0)
   #--- ボタン生成
    Button =\
     ttk.Button(MtroPage, text="           I love it           ")

    #---  ボタン配置
    # 空白
    # ボタン
    Button.pack(fill = 'x' ,padx=30,side='top')
    
    #--- ボタン生成2
    Button =\
     ttk.Button(MtroPage, text="           No Thanks           ")

    #---  ボタン配置
    # 空白
    # ボタン
    Button.pack(fill = 'x' ,padx=30,side='top')
    #--- ボタン生成3    
    Button =\
     ttk.Button(MtroPage, text="           modoru by Mtro           ", command=lambda : changePage(HOME))

    #---  ボタン配置
    # 空白
    # ボタン
    Button.pack(fill = 'x' ,padx=30,side='top')

    # MetroPageを配置
    MtroPage.grid(row=0, column=0, sticky="nsew")
    
        #-----------------------------------PeSt（演奏開始）---------------------------------
    ### PeSt用のFrameを生成
    PeSt = tkinter.Frame(window)

    #---  ラベル生成
    spaceLabel1 = [tkinter.Label(TUREPage, text="") for column in range(5)]
    # タイトル
    titleLabelFont  = ("Helevetice", 32, "bold")
    titleLabel =\
        ttk.Label(PeSt, text="Silent Recorder", font=titleLabelFont)
    #---  ラベル配置
    # タイトル
    titleLabel.pack()
    
    ###  空白
    #---  ラベル生成
    spaceLabel1 = [tkinter.Label(PeSt, text="") for column in range(5)]
    #---  ラベル配置
    # 空白
    for index in range(5):
        spaceLabel1[index].pack()
    # タイトル
    #titleLabel.pack()

    ### フレーム表示
    #---  フレーム生成
    frame = ttk.Frame(PeSt)
    #---  フレーム配置
    frame.pack()

    ### ユーザー名入力表示
    #--- ラベル生成
    # 空白
    spaceLabel2 = [tkinter.Label(frame, text="") for column in range(3)]

    #--- ラベル配置
    # 空白
    for index in range(3):
        spaceLabel2[index].grid(row=index, column=0)
    # ユーザー名
    #userNameLabel.grid(row=4, column=0)
    
    Button =\
     ttk.Button(PeSt, text="           modoru by PeSt          ", command=lambda : changePage(doPage))

    #---  ボタン配置
    # 空白
    # ボタン
    Button.pack(fill = 'x' ,padx=30,side='top')

    # PeStを配置
    PeSt.grid(row=0, column=0, sticky="nsew")
    
    
    # HOMEを上位層にする
    HOME.tkraise()

    # プログラムを始める
    window.mainloop()

#====================================================================================
# 本体処理
#====================================================================================
if __name__ == "__main__":
    main()

