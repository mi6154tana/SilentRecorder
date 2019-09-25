import tkinter as tk
import time
import json
import sys
import threading
# from udp_com import UdpCom as uc
from play_sound import PlaySound as ps
#from gpio_in import GpioIn as gi

class NormalPlay:
    def __init__(self, cv, root):
        self.cv = cv
        self.root = root
        self.flag = 0
        #self.button = gi()

        # 再帰回数の設定
        sys.setrecursionlimit(6000)

        # sound dataの読み込み_試験用
        self.sound_data = self.__read_file()

        # 受信の準備
        # self.udp_data = uc()
        # 音を出す準備
        self.sound = ps()

        # self.thread_wi = threading.Thread(target=self.__wait_input)#並行処理で入力を待つ

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
        '''
        if self.button.gpio_input() == 0:
            udp_data.play_stop()
            self.root.quit()
            return
            
        '''

        """
        if self.button.gpio_input() == 3:
            with open("config.json","r") as json_file:
                config_dict = json.load(json_file)
            if config_dict["record_flag"] == "ON":
                config_dict["record_flag"] = "OFF"
            else:
                config_dict["record_flag"] = "ON"

            with open("config.json","w") as json_file:
                json.dump(config_dict,json_file)
        """

        if sdi >= len(self.sound_data) and self.flag == 0:
            sdi = sdi - 1
            self.flag = 1

        # 描画していたリコーダーを削除
        self.cv.delete('recorder')
        # 描画していたonoff_labelを削除
        self.cv.delete('rf_text')
        # 描画していたsound_volumeを削除
        self.cv.delete('sd_volume')

        # onfoo label表示
        self.__draw_onoff_label()

        # sound_volume表示
        self.__draw_sound_volume(sdi)

        # リコーダー本体(表)
        self.cv.create_polygon(110, 40, 110, 280, 180, 280, 180, 40, fill="blue", tag='recorder')

        # リコーダー本体(裏)
        self.cv.create_polygon(30, 40, 30, 280, 100, 280, 100, 40, fill="blue", tag='recorder')
        
        #受信
        #rcv_data = self.udp_data.rcv_input()
        #rcv_data_s = rcv_data.split(':')
        #self.sound_data[sdi]['volume'] = rcv_data_s[0]
        #self.sound_data[sdi]['hole_data'] = rcv_data_s[1]

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

        #音を出す
        #self.sound.sr_play(self.udp_data.return_input())#通信時
        self.sound.sr_play(self.sound_data[sdi]['hole_data'], int(self.sound_data[sdi]['volume']))

        if self.flag == 0:
            self.root.after(100, self.__draw_recorder, sdi+1)
        elif self.flag == 1:
            del self.sound
            # udp_data.play_stop()
            self.root.quit()
            return

    def __write_record_flag(self, json_obj):
        with open('config.json', 'w') as f:
            json.dump(json_obj,f,ensure_ascii=False)

    def __get_record_flag(self):
        with open('config.json', 'r') as f:
            conf_data = json.load(f)
        return conf_data

    def __draw_onoff_label(self):
        rf_text = self.__get_record_flag()
        self.cv.create_text(250, 30, text=rf_text['record_flag'], tag='rf_text')

    def __draw_sound_volume(self, sdi):
        # volumeの枠作成
        self.cv.create_polygon(400, 40, 400, 280, 480, 280, 480, 40, tag='sd_volume', fill='', outline='black')
        # volumeの量表示
        self.cv.create_polygon(400, 280-int(self.sound_data[sdi]['volume']), 400, 280, 480, 280, 480, 280-int(self.sound_data[sdi]['volume']), fill="blue", tag='sd_volume')
        # 値表示
        self.cv.create_text(440, 280-int(self.sound_data[sdi]['volume'])/2, text=self.sound_data[sdi]['volume'], tag='sd_volume')

    def __wait_input(self):
        while 1:
            print('>>')
            input_num = int(sys.stdin.readline().rstrip())
            if input_num == 0:
                # self.thread_wi.join()
                #self.thread_wi = None
                break
            if input_num == 3:
                rf_text = self.__get_record_flag()
                if rf_text['record_flag'] == 'OK':
                    rf_text['record_flag'] == 'OFF'
                elif rf_text['record_flag'] == 'OFF':
                    rf_text['record_flag'] == 'ON'
                self.__write_record_flag(rf_text)
                self.cv.delete('rf_text')
                self.__draw_onoff_label()


    def npmain(self):
        # self.thread_wi.start()
        # self.udp_data.zero_start(1)#演奏デバイスに送信指示
        self.__draw_recorder()
        self.root.mainloop()
        print('end')