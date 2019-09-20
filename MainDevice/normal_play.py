import tkinter as tk
import time
import json
import sys

class NormalPlay:
    def __init__(self, cv, root):
        self.cv = cv
        self.root = root
        self.flag = 0

        # 再帰回数の設定
        sys.setrecursionlimit(6000)

        # sound dataの読み込み
        self.sound_data = self.__read_file()

    def __read_file(self):
        with open('Recorder.txt', 'r') as f:
            read_text = f.read()
        sound_data = []
        for i in read_text.split('\n'):
            split_i = i.split(':')
            try:
                sound_dict = {}
                sound_dict['volume'] = int(split_i[0])
                sound_dict['hole_data'] = split_i[1]
                sound_data.append(sound_dict)
            except ValueError:
                pass
        return sound_data

    def __draw_recorder(self, sdi=0):
        if sdi >= len(self.sound_data) and self.flag == 0:
            sdi = sdi - 1
            self.flag = 1

        # 描画していたリコーダーを削除
        self.cv.delete('recorder')

        # 裏の描写を隠す
        # self.cv.create_polygon(0, 0, 0, 300, 512, 300, 512, 0, fill="white", tag='recorder')

        # リコーダー本体(表)
        self.cv.create_polygon(110, 40, 110, 280, 180, 280, 180, 40, fill="blue", tag='recorder')

        # リコーダー本体(裏)
        self.cv.create_polygon(30, 40, 30, 280, 100, 280, 100, 40, fill="blue", tag='recorder')
        
        # リコーダー穴(表)
        for i,hd in zip(range(7), self.sound_data[sdi]['hole_data'][0:7][::-1]):
            if hd == '1':
                self.cv.create_oval(142.5-10, 63+32*i-10, 142.5+10, 63+32*i+10, fill="black", tag='recorder')
            if hd == '0':
                self.cv.create_oval(142.5-10, 63+32*i-10, 142.5+10, 63+32*i+10, tag='recorder')
        # リコーダー穴(裏)
        if self.sound_data[sdi]['hole_data'][7] == '1':
            self.cv.create_oval(62.5-10, 63-10, 62.5+10, 63+10, tag='recorder', fill='black')
        if self.sound_data[sdi]['hole_data'][7] == '0':
            self.cv.create_oval(62.5-10, 63-10, 62.5+10, 63+10, tag='recorder')
        
        if self.flag == 0:
            self.root.after(10, self.__draw_recorder, sdi+1)
            self.root.mainloop()
        elif self.flag == 1:
            return

    def __draw_onoff_label(self):
        with open('config.json', 'r') as f:
            conf_data = json.load(f)
        self.cv.create_text(250, 30, text=conf_data['match_check'])

    def npmain(self):
        self.__draw_onoff_label()
        self.__draw_recorder()
        print('end')
        # for sd in self.sound_data:
        #     self.__draw_recorder(sd)
        # self.__draw_recorder({'volume': 1, 'hole_data': '00001111'})
        # self.__draw_recorder({'volume': 1, 'hole_data': '00001011'})
        # self.__draw_recorder({'volume': 1, 'hole_data': '00101111'})
        # self.__draw_recorder({'volume': 1, 'hole_data': '00001110'})