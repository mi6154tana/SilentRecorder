# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.

import socket
import struct
from contextlib import closing

class UdpCom:
    
    def __init__(self):
        self.HOST = '192.168.11.10'
        self.SEND_PORT = 60000
        
        self.RCV_IP = ""
        self.RCV_PORT = 60000

        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_rcv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_rcv.bind((self.RCV_IP, self.RCV_PORT))

        #self.sock_rcv.setblocking(0)#いるかも
    
    def zero_start(self, mode):
        #mode == 0 shutdown
        #mode == 1 play_start
        mode_s = struct.pack('>i', mode)
        self.sock_send.sendto(mode_s, (HOST, SEND_PORT))

    def rcv_input(self):
        b_data, addr = self.sock_rcv.recvfrom(1024)
        data = str(b_data)
        data_s = data.strip("b'").strip("'")
        print(data_s)
        return data_s

    def play_stop(self):
        sock_send.sendto('stop', (HOST, SEND_PORT))

    def close_sock(self):
        #with closing(self.sock):
        self.sock.close()
        print('close connection...')


