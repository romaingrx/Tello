#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 25 December 2019
"""

import socket
import threading
import sys
import multiprocessing

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_TYPES = {EXIT_SUCCESS:'successful', EXIT_FAILURE:'failure'}

class Tello(object):

    def __init__(self, host_address='', host_port=9000):
        self.host_address = host_address
        self.host_port = host_port
        self.localaddr = (self.host_address,self.host_port)
        self.tello_address = '192.168.10.1'
        self.tello_port = 8889
        self.telloaddr = (self.tello_address,self.tello_port)
        self.sockfd = None
        self.processes = []

    def connect(self):
        print('\n... Initialization ...\n')
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockfd.bind(self.localaddr)
        self.recvProcess = multiprocessing.Process(target=self.recv)
        self.recvProcess.start()
        self.processes.append(self.recvProcess)

    def fromKeyboard(self):
        while True:
            try:
                msg = input('')
                if not msg:
                    break
                if 'stop' in msg:
                    self._exit(EXIT_SUCCESS)
                    break
                msg = msg.encode(encoding="utf-8")
                sent = self.sockfd.sendto(msg, self.telloaddr)
            except KeyboardInterrupt:
                self._exit(EXIT_SUCCESS)
                break


    def recv(self):
        while True:
            try:
                data, server = self.sockfd.recvfrom(1518)
                print(data.decode(encoding="utf-8"))
            except Exception as e:
                self._exit(EXIT_FAILURE)
                break

    def _exit(self, type:int):
        print('\n... exit %s ....\n'%EXIT_TYPES[type])
        for process in self.processes:
            process.terminate()
        self.sockfd.close()
        sys.exit(type)

if __name__=='__main__':
    tello = Tello()
    tello.connect()
    tello.fromKeyboard()
