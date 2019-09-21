# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.

import socket
import struct
from contextlib import closing

class UdpRcv:
    
    def __init__(self):
        self.UDP_IP = ""
        self.UDP_PORT = 60000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
    
    def return_input(self):
        data, addr = self.sock.recvfrom(1024)
        print(data)
        return data

    def close_sock(self):
        #with closing(self.sock):
        self.sock.close()
        print('close connection...')


