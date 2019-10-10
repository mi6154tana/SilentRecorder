# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.
import datetime
import json
import os
import shutil
import os

class OpeRecording:
    def __init__(self):
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        print('call OpeRecording')
        self.file_name = nowDirectoryPath + 'udp_input.txt'
    
    def open_file(self):
        print('call open ', self.file_name)
        self.fp = open(self.file_name, 'w')
    
    def write_head_data(self, bpm, ordinal_num, radix):
        data = bpm + ' ' + ordinal_num + ' ' + radix + '\n'
        self.fp.write(data)

    def write_recording(self, v_data, f_data):
        data = v_data + ':' + f_data + '\n'
        self.fp.write(data)
    
    def write_stop(self, m_name):
        print('close ', self.file_name)
        self.fp.close()
        rf_text = self.__get_record_flag()
        if rf_text['record_flag'] == 'ON':
            dt_now = datetime.datetime.now()
            nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
            record_name = nowDirectoryPath + m_name + str(dt_now.year) + str(dt_now.month) + str(dt_now.day) + str(dt_now.hour) +  str(dt_now.minute) +  str(dt_now.second) + '.txt'
            shutil.copyfile(nowDirectoryPath + 'udp_input.txt', record_name)
            shutil.move(record_name, nowDirectoryPath + 'Recording/')

    
    def del_recording(self, data_name):
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        print('Deleat : ' + data_name)
        os.remove(nowDirectoryPath + 'Recording/' + data_name)
    
    def __get_record_flag(self):
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        with open(nowDirectoryPath +'config.json', 'r') as f:
            conf_data = json.load(f)
        return conf_data
