# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.
#import RPi.GPIO as GPIO
import tkinter as tk
import time
from PIL import Image, ImageTk
from gpio_in import GpioIn as gi #RaspberryPiでの動作確認
from create_page import CreatePage as cp
from ope_recording import OpeRecording as o_re
import page_func as pf
import json
import os
from collections import OrderedDict
import codecs
#from udp_com import UdpCom as uc #RaspberryPiでの動作確認 and 演奏デバイスと通信時

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
    'POWER',
    'DELEAT_OR_PLAY_RECORDING'
]

trans_list = [#行はpagesに格納されているインデックス番号に対応、配列の中身は移動先のページのインデックス番号
        [0, 1, 2, 4, 6, 7],#0:ホーム　最左列は戻る（左ボタン）での対応先、コンテンツは１～番号が振られており、選択されていればそこに移動
        [0],            #1:通常演奏　用意されていなければ、先に進めない
        [0, 3],         #2:楽譜リスト
        [2],            #3:正確性診断
        [0, 8],         #4:演奏記録一覧
        [4],            #5:演奏記録再生
        [0],            #6:設定
        [0],            #7:電源
        [4, 5]          #8:記録を消すか否か
    ]

button = None
p_position = 0#現在のページ
c_select = 1
se_file = ''
#udp_data = uc()#RaspberryPiでの動作確認 and 演奏デバイスと通信時

def change_page(button_in):
    global p_position, c_select, se_file
    
    #button_in = int(input('>>'))#PCでの動作確認
    button_in = button.gpio_input()#PaspberryPiでの動作確認
    
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

        if p_position == 8 and c_select == 2:#記録を消す
            ope = o_re()
            ope.del_recording(se_file)
            pages[trans_list[p_position][0]].raise_page()
            pages[trans_list[p_position][0]].draw_select(1)
            p_position = trans_list[p_position][0]
            c_select = 1

        elif p_position == 7:#仮の終了
            #udp_data.zero_start(0)#RaspberryPiでの動作確認 and 演奏デバイスと通信時
            root.destroy()
            if c_select == 1:
                os.system('sudo shutdown -h now')
            return

        elif p_position == 6:
            #設定ファイル書き換え
            nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
            with open(nowDirectoryPath + "config.json","r") as config_file:
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

            if c_select == 4:
                json_obj["Volume"] = str(int(json_obj["Volume"]) + 1)
                if int(json_obj["Volume"])  == 3:
                    json_obj["Volume"] = "0"
                print(json_obj["Volume"])
                #print(select_volumes[int(json_obj["Volume"])])

            with codecs.open(nowDirectoryPath + "config.json","w","utf-8") as writing_config_file:
                json.dump(json_obj,writing_config_file,ensure_ascii=False)

            #contents更新
            pages[p_position].contents = pages[p_position]._get_list_cons(p_position)
            pages[p_position].draw_cons()
            #print(pages[p_position].contents)

        else:
            if p_position == 2 or p_position == 4 or p_position == 8:
                if len(pages[p_position].contents) > 0:
                    se_file = pages[p_position].contents[pages[p_position].d_positoin + c_select - 1]#要改良
                    #pages[8].set_file_name(se_file)
                    if p_position == 8:
                        se_file = se_file.strip("を再生")
                        se_file = se_file.strip("を消去")
                    pages[trans_list[p_position][1]].set_file_name(se_file)
                    se_file += '.txt'
                else:
                    se_file = ''
            if len(trans_list[p_position]) == 2:#移動先が一つだけの時
                if len(pages[p_position].contents) > 0:
                    get_con = pages[p_position].contents[pages[p_position].d_positoin + c_select - 1]#要改良
                else:
                    get_con = ''
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
        #root.after(100, change_page, -1)#PCでの動作確認
        root.after(100, change_page, button.gpio_input())#PaspberryPiでの動作確認

def main():
    global root, pages, button

    button = gi() #RaspberryPiでの動作確認
    
    root = tk.Tk()

    # ウィンドウタイトルを決定
    root.title("SilentRecorder")
    # ウィンドウの大きさを決定
    root.geometry("512x300")#"512x300"
    root.attributes("-fullscreen", True)

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
