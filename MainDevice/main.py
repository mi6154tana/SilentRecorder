# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.
#import RPi.GPIO as GPIO
import tkinter as tk
import time
from PIL import Image, ImageTk
#from gpio_in import GpioIn as gi
from create_page import CreatePage as cp
import page_func as pf
import json
import os
from collections import OrderedDict

root = None
pages = []
page_names = [
    'HOME',
    'NORMAL_PLAY',
    'SCORE_LIST',
    'JUDGE_PLAY',
    'RECORDING_LIST',
    'PLAY_RECORDING',
    'SETTING',
    'POWER'
]

trans_list = [#行はpagesに格納されているインデックス番号に対応、配列の中身は移動先のページのインデックス番号
        [0, 1, 2, 4, 6, 7],#0:ホーム　最左列は戻る（左ボタン）での対応先、コンテンツは１～番号が振られており、選択されていればそこに移動
        [0],            #1:通常演奏　用意されていなければ、先に進めない
        [0, 3],         #2:楽譜リスト
        [2],            #3:正確性診断
        [0, 5],         #4:演奏記録一覧
        [4],            #5:演奏記録再生
        [0],            #6:設定
        [0]             #7:電源
    ]

button = None
p_position = 0#現在のページ
c_select = 1

'''
def gpio_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4,GPIO.OUT)
    GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(25,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

def gpio_input():
    if GPIO.input(18) == GPIO.HIGH:
        print(0)
        return 0
    elif GPIO.input(23) == GPIO.HIGH:
        print(1)
        return 1
    elif GPIO.input(24) == GPIO.HIGH:
        print(2)
        return 2
    elif GPIO.input(25) == GPIO.HIGH:
        print(3)
        return 3
    else:
        print(-1)
        return -1
'''

def change_page(button_in):
    global p_position, c_select
    
    button_in = int(input('>>'))#PCでの動作確認
    #button_in = button.gpio_input()
    
    if button_in == 0:#左
        pages[trans_list[p_position][0]].raise_page()
        pages[trans_list[p_position][0]].draw_select(1)
        p_position = trans_list[p_position][0]
        c_select = 1

    elif button_in == 1 and p_position != 1:#上
        if c_select == 1 and pages[p_position].d_positoin > 0:
            pages[p_position].d_positoin -= 1
            pages[p_position].draw_cons() 
        elif c_select != 1:
            c_select -= 1
        pages[p_position].draw_select(c_select)

    elif button_in == 2 and p_position != 1:#下
        if len(pages[p_position].contents) >= c_select + 1: 
            c_select += 1
            if c_select > 5:
                c_select = 5
                if len(pages[p_position].contents) >= pages[p_position].d_positoin + 6:
                    pages[p_position].d_positoin += 1
            pages[p_position].draw_cons()
        pages[p_position].draw_select(c_select)
    
    elif button_in == 3:#右
        if p_position == 7:#仮の終了
            root.destroy()
            if c_select == 1:
                os.system('sudo shutdown -h now')
            return

        if p_position == 6:
            #設定ファイル書き換え
            with open("./config.json") as config_file:
                json_obj = json.load(config_file,object_pairs_hook=OrderedDict)

            if c_select == 1:
                if json_obj["metronom"] == "ON":
                    json_obj["metronom"] = "OFF"
                else:
                    json_obj["metronom"] = "ON"

            if c_select == 2:
                if json_obj["record_flag"] == "ON":
                    json_obj["record_flag"] = "OFF"
                else:
                    json_obj["record_flag"] = "ON"

            if c_select == 3:
                if json_obj["Mode"] == "A":
                    json_obj["Mode"] = "B"
                else:
                    json_obj["Mode"] = "A"

            with open("./config.json","w") as writing_config_file:
                json.dump(json_obj,writing_config_file,ensure_ascii=False)

            #test
            # print("==============================================================")
            # test = open("./config.json","r")
            # print(json.load(test))
            # test.close()
            # print("==============================================================")

            #contents更新
            pages[p_position].contents = pages[p_position]._get_list_cons(p_position)
            pages[p_position].draw_cons()
            #print(pages[p_position].contents)


        if len(trans_list[p_position]) == 2:#移動先が一つだけの時
            get_con = pages[p_position].contents[pages[p_position].d_positoin + c_select - 1]#要改良
            print('select : ' + get_con)
            pages[trans_list[p_position][1]].raise_page()
            if trans_list[p_position][1] != 1 and trans_list[p_position][1] != 3 and trans_list[p_position][1] != 5:
                pages[trans_list[p_position][1]].draw_select(1)
            p_position = trans_list[p_position][1]
            c_select = 1
            # pf.select_func(p_position, get_con)#そのページ専用関数を発動
        elif len(trans_list[p_position]) != 1:#???
            pages[trans_list[p_position][c_select]].raise_page()
            #pages[trans_list[p_position][c_select]].draw_select(1)
            p_position = trans_list[p_position][c_select]
            # pf.select_func(p_position, 'None')#そのページ専用関数を発動
            c_select = 1

    
    if button_in == 7777:
        root.destroy()
    else:
        root.after(100, change_page, -1)#PCでの動作確認
        #root.after(100, change_page, button.gpio_input())

def main():
    global root, pages, button

    #gpio_init()
    #button = gi()
    
    root = tk.Tk()

    # ウィンドウタイトルを決定
    root.title("SilentRecorder")
    # ウィンドウの大きさを決定
    root.geometry("512x300")
    #window.attributes("-fullscreen", True)

    # ウィンドウのグリッドを 1x1 にする
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    #home = cp(root, 'HOME', home_cons)
    for i in range(len(page_names)):
        pages.append(cp(root, page_names[i], i))

    pages[0].raise_page()

    root.after(1000, change_page, -1)
    #change_page()
    #test_p.raise_page()
    root.mainloop()

if __name__ == '__main__':
    main()