# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 17:43:55 2019

@author: HCHO
"""

from socket import *
import json
import time

address='127.0.0.1'   #服务器的ip地址
address='193.112.96.116'


port = 8002
buffsize=1024        #接收数据的缓存大小
#s=socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
s=socket(AF_INET, SOCK_STREAM)
s.connect((address,port))
while True:
    
    senddata=input('想要发送的数据：')
    #senddata=json.dumps({'f':6})
    if senddata=='exit':
        s.send(senddata.encode())
        break
    s.send(senddata.encode())
    
    #s.send()
    #recvdata=s.recv(buffsize).decode('utf-8')
    #recvdata=s.recv(buffsize).decode('utf-8')
    #print(recvdata)
    #time.sleep(0.1)
s.close()