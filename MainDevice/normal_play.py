import tkinter as tk
import time
import json
import sys
import threading
import os
from udp_com import UdpCom as uc #RaspberryPiでの動作確認
from play_sound import PlaySound as ps
from ope_recording import OpeRecording as o_re
from gpio_in import GpioIn as gi #RaspberryPiでの動作確認

class NormalPlay:
    def __init__(self, cv, root):
        self.damy_mode = 0 #演奏デバイスと通信せずに動かす
        self.center_adj = 100 #中央寄せ調整用
        self.draw_mag = 2.0 #フルスクリーン時、表示するディスプレイに合わせるため
        self.cv = cv
        self.root = root
        self.flag = 0
        self.button = gi()#PaspberryPiでの動作確認

        # 再帰回数の設定
        sys.setrecursionlimit(6000)

        # sound dataの読み込み_試験用
        # self.sound_data = self.__read_file()
        self.sound_data = {}

        # 受信の準備
        if not self.damy_mode:
            self.udp_data = uc()#PaspberryPiでの動作確認

        # 音を出す準備
        self.sound = ps()

        #記録をとる準備
        self.write_rec = o_re()
        self.write_rec_flag = 0

        # self.thread_wi = threading.Thread(target=self.__wait_input)#並行処理で入力を待つ

    def __read_file(self):
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        with open(nowDirectoryPath + 'damy_input.txt', 'r') as f:
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
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        
        if self.button.gpio_input() == 0:#PaspberryPiでの動作確認
            if not self.damy_mode:
                self.udp_data.play_stop()
            if self.write_rec_flag == 1:
                self.write_rec.write_stop('user')
            self.flag = 1
            self.root.quit()
            return
        
        if self.button.gpio_input() == 3:#PaspberryPiでの動作確認
            with open(nowDirectoryPath + "config.json","r") as json_file:
                config_dict = json.load(json_file)
            if config_dict["record_flag"] == "ON":
                config_dict["record_flag"] = "OFF"
            else:
                config_dict["record_flag"] = "ON"

            with open(nowDirectoryPath + "config.json","w") as json_file:
                json.dump(config_dict,json_file)
       
        # if self.flag == 0:
        #     sdi = sdi - 1
        #     self.flag = 1

        # 描画していたリコーダーを削除
        self.cv.delete('recorder')
        # 描画していたonoff_labelを削除
        self.cv.delete('rf_text')
        # 描画していたsound_volumeを削除
        self.cv.delete('sd_volume')

        if not self.damy_mode:
            #受信　PaspberryPiでの動作確認　
            rcv_data = self.udp_data.rcv_input()
            rcv_data_s = rcv_data.split(':')
            self.sound_data['volume'] = rcv_data_s[0]
            self.sound_data['hole_data'] = rcv_data_s[1]
            print(self.sound_data)

        # onfoo label表示
        self.__draw_onoff_label()
        # sound_volume表示
        self.__draw_sound_volume(sdi)
        # 音階表示
        self.__draw_sound_musicscale(sdi)

        # リコーダー本体(表)
        self.cv.create_polygon(self.center_adj + 110*self.draw_mag,40*self.draw_mag, self.center_adj + 110*self.draw_mag,280*self.draw_mag, self.center_adj + 180*self.draw_mag,280*self.draw_mag, self.center_adj + 180*self.draw_mag,40*self.draw_mag, fill="#437ecc", tag='recorder')

        # リコーダー本体(裏)
        self.cv.create_polygon(self.center_adj + 30*self.draw_mag,40*self.draw_mag, self.center_adj + 30*self.draw_mag,280*self.draw_mag, self.center_adj + 100*self.draw_mag,280*self.draw_mag, self.center_adj + 100*self.draw_mag, 40*self.draw_mag, fill="#437ecc", tag='recorder')
        
        # リコーダー穴(表)
        for i,hd in zip(range(7), self.sound_data['hole_data'][0:7][::-1]):
            if hd == '1':
                self.cv.create_oval(self.center_adj + (142.5-10)*self.draw_mag, (63+32*i-10)*self.draw_mag, self.center_adj + (142.5+10)*self.draw_mag, (63+32*i+10)*self.draw_mag, fill="black", tag='recorder')
            if hd == '0':
                self.cv.create_oval(self.center_adj + (142.5-10)*self.draw_mag, (63+32*i-10)*self.draw_mag, self.center_adj + (142.5+10)*self.draw_mag, (63+32*i+10)*self.draw_mag, tag='recorder')
        # リコーダー穴(裏)
        if self.sound_data['hole_data'][7] == '1':
            self.cv.create_oval(self.center_adj + (62.5-10)*self.draw_mag, (63-10)*self.draw_mag, self.center_adj + (62.5+10)*self.draw_mag, (63+10)*self.draw_mag, tag='recorder', fill='black')
        if self.sound_data['hole_data'][7] == '0':
            self.cv.create_oval(self.center_adj + (62.5-10)*self.draw_mag, (63-10)*self.draw_mag, self.center_adj + (62.5+10)*self.draw_mag, (63+10)*self.draw_mag, tag='recorder')

        #音を出す
        self.sound.sr_play(self.sound_data['hole_data'], int(self.sound_data['volume']))
        #記録を残す
        if self.write_rec_flag:
            self.write_rec.write_recording(str(self.sound_data['volume']), str(self.sound_data['hole_data']))

        if self.flag == 0:
            self.root.after(30, self.__draw_recorder, sdi+1)#in udp_com sleep is 25
        elif self.flag == 1:
            del self.sound
            if not self.damy_mode:
                self.udp_data.play_stop()#PaspberryPiでの動作確認
            if self.write_rec_flag == 1:
                self.write_rec.write_stop('user')
            self.root.quit()
            return
        
    def __write_record_flag(self, json_obj):
        with open(nowDirectoryPath + 'config.json', 'w') as f:
            json.dump(json_obj,f,ensure_ascii=False)

    def __get_record_flag(self):
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        with open(nowDirectoryPath + 'config.json', 'r') as f:
            conf_data = json.load(f)
        return conf_data

    def __draw_onoff_label(self):
        rf_text = self.__get_record_flag()
        # 枠表示
        self.cv.create_rectangle(self.center_adj + 220*self.draw_mag, 40*self.draw_mag, self.center_adj + 300*self.draw_mag, 120*self.draw_mag)
        # on,offの表示
        self.cv.create_text(self.center_adj + 260*self.draw_mag, 80*self.draw_mag, font=("Purisa", int(20*self.draw_mag)), text='記録\n'+rf_text['record_flag'], tag='rf_text')
        #記録のオンオフ
        if self.write_rec_flag == 0 and rf_text['record_flag'] == 'ON':
            self.write_rec_flag = 1
            self.write_rec.open_file()
            self.write_rec.write_head_data('60', '4', '4')
        elif self.write_rec_flag == 1 and rf_text['record_flag'] == 'OFF':
            self.write_rec_flag = 0
            self.write_rec.write_stop('user')

    def __draw_sound_volume(self, sdi):
        # volumeの枠作成
        self.cv.create_polygon(self.center_adj + 360*self.draw_mag,40*self.draw_mag, self.center_adj + 360*self.draw_mag,280*self.draw_mag, self.center_adj + 440*self.draw_mag,280*self.draw_mag, self.center_adj + 440*self.draw_mag,40*self.draw_mag, tag='sd_volume', fill='', outline='black')
        # volumeの量表示
        self.cv.create_polygon(self.center_adj + 360*self.draw_mag,(280-int(self.sound_data['volume'])*280/3095)*self.draw_mag, self.center_adj + 360*self.draw_mag,280*self.draw_mag, self.center_adj + 440*self.draw_mag,280*self.draw_mag, self.center_adj + 440*self.draw_mag,(280-int(self.sound_data['volume'])*280/3095)*self.draw_mag, fill="blue", tag='sd_volume')
        # 値表示
        self.cv.create_text(self.center_adj + 400*self.draw_mag, (280-int(self.sound_data['volume'])/2)*self.draw_mag, text=self.sound_data['volume'], tag='sd_volume')
    
    def __draw_sound_musicscale(self, sdi):
        fingering_models = {
            '11111111':'ド',    # do
            '01111111':'レ',    # re
            '00111111':'ミ',    # mi
            '00011111':'ファ',   # fa
            '00001111':'ソ',    # sol
            '00000111':'ラ',    # la
            '00000011':'シ',    # si
            '00000101':'^ド',   # do8va
            '00000100':'^レ',   # re8va
            '00111110':'^ミ'    # mi8va
        }
        hole_data = self.sound_data['hole_data']
        try:
            # 枠の表示
            self.cv.create_rectangle(self.center_adj + 230*self.draw_mag,130*self.draw_mag, self.center_adj + 290*self.draw_mag,170*self.draw_mag)
            # 音階の表示
            self.cv.create_text(self.center_adj + 260*self.draw_mag, 150*self.draw_mag, font=("Purisa", int(20*self.draw_mag)), text=fingering_models[hole_data], tag='recorder')
        except:
            pass

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
        if not self.damy_mode:
            #演奏デバイスに送信指示 PaspberryPiでの動作確認
            print('read mode')
            pd_mode_text = self.__get_record_flag()
            print('finish read mode. mode = ', pd_mode_text['Mode'])
            if pd_mode_text['Mode'] == 'B':
                print('zero start B')
                self.udp_data.zero_start(2)
                print('connnected')
            else:
                print('zoro start A')
                self.udp_data.zero_start(1)
                print('connected A')
        self.__draw_recorder()
        self.root.mainloop()
        print('end')
