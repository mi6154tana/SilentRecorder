# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.
import datetime
import json
import os

class OpeRecording:
    def __init__(self):
        self.file_name = './udp_input.txt'
    
    def open_file(self):
        self.fp = open(self.file_name, 'w')
    
    def write_recording(self, v_data, f_data):
        data = v_data + ':' + f_data + '\n'
        self.fp.write(data)
    
    def write_stop(self, m_name):
        self.fp.close()
        rf_text = self.__get_record_flag()
        if rf_text['record_flag'] == 'ON':
            dt_now = datetime.datetime.now()
            record_name = m_name + str(dt_now) + '.txt'
            shutil.copy('./udp_input.txt', record_name)

    
    def del_recording(self, data_name):
        print('Deleat : ' + data_name)
        os.remove('./Recording/' + data_name)
    
    def __get_record_flag(self):
        with open('config.json', 'r') as f:
            conf_data = json.load(f)
        return conf_data





