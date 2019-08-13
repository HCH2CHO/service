# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 17:38:08 2019

@author: HCHO
"""

from socket import *
import json

address='127.0.0.1'     #监听哪些网络  127.0.0.1是监听本机 0.0.0.0是监听整个网络
#address=''
port=12580             #监听自己的哪个端口
buffsize=1024          #接收从客户端发来的数据的缓存区大小
s = socket(AF_INET, SOCK_STREAM)
s.bind((address,port))
s.listen(1)     #最大连接数
test=True
while test:
    clientsock,clientaddress=s.accept()
    print('connect from:',clientaddress)
    #传输数据都利用clientsock，和s无关
    while True:  
        recvdata=clientsock.recv(buffsize).decode('utf-8')
        if recvdata=='exit' or not recvdata:
            test=False
            break
        senddata=recvdata+'from sever'
        clientsock.send(senddata.encode())
clientsock.close()
s.close()
