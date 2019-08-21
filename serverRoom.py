# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:28:50 2019

@author: HCHO
"""

#返回参数时会阻塞其他客户端
#断开客户端会致使服务端崩溃
import select
import socket
import sys
import time
import json
# 创建 TCP/IP 套接字
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# 绑定套接字到端口
# ip在云服务器中运行时为''
port = 8002
ip = ""

server_address = (ip, port)
server.bind(server_address)

# 监听即将到来的连接
server.listen(5)

inputs = [server]
outputs=[]
abnormal_msg=[]

#消息
#message_queues = {}

#速度档位,0为停止,1为慢速,2为中速,3为快速
speed=1
alarm=0
light=0
light_count=0
#加载点数据
file_data=open('route.txt','r',encoding='utf-8')
point_data=[]
point_count=0
line=file_data.readline()
while line:
    line_list=line.strip().split(',')
    #if(line_list[1]=='2'):
    if(len(line_list)==4):
        #json数据字符串化
        point_data.append(json.dumps({"x":line_list[1],"y":line_list[2]}) )
    line=file_data.readline()


#是否关闭
bool_continue=True

while bool_continue:
    #等待至少有一个套接字准备好了进行后续处理。
    #print('waiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs,outputs,abnormal_msg,1)
    #inputs 处理
    for s in readable:
        if s is server:
            # 可读的套接字需要准备好接收连接。
            connection, client_address = s.accept()
            print('connection from', client_address)
            #connection.setblocking(0)
            inputs.append(connection)
            #添加输出对象
            outputs.append(connection)
            #把我们想发送的数据队列给它。
            #message_queues[connection] = queue.Queue()
        else:
            try:
                data = s.recv(1024).decode('utf-8')
                #data_type为Light,Alarm,Speed,Exit
                if data:
                    data_type,data_value=data.split(':')
                    print(data_type,data_value)
                    if data_type=='E':
                        bool_continue=False
                    elif data_type=='S':
                        speed=int(data_value)
                    elif data_type=='A':
                        alarm=int(data_value)
                    elif data_type=='L':
                        light=int(data_value)
                        light_count=100
                    else:
                        print('wrong type')
                else:
                    print('wrong input')
            except Exception as e:
                print(e)
                inputs.remove(s)
				
                # 一个有数据的可读客户端
                #print('  received {!r} from {}'.format(data, s.getpeername()), file=sys.stderr,)
                #message_queues[s].put(data)
                #speed=data.decode('utf-8')
                # 添加到输出列表用来做响应
                #if s not in outputs:
                #    outputs.append(s)
            '''
            else:
                # 空结果表明要关闭连接
                #print('  closing', client_address,file=sys.stderr)
                # 停止监听该链接的输入
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                # 删除这个消息队列
                #del message_queues[s]
            '''    
    # outputs 处理
    for s in writable:
        try:
            #next_msg = message_queues[s].get_nowait()
            if(point_count>=len(point_data)):
                point_count=point_count-len(point_data)
            position_msg='{"type":"position","data":'+point_data[point_count]+'}*'
            speed_msg='{"type":"speed","data":'+str(int(speed*3.6))+'}*'
            point_count=point_count+int(speed)
            #位置信息、速度信息            
            #s.send(position_msg.encode())
            #s.send(speed_msg.encode())
            #报警信息、红绿灯信息
            if(alarm != 0):
                if alarm>0 and alarm <5:
                    alarm_msg='{"type":"alarm","data":'+str(alarm)+'}*'
                    s.send(alarm_msg.encode())
                alarm=0
                
            if(light_count !=0):                
                if light==1:
                    light_msg='{"type":"light","data":{"left":"red","front":"red","right":"green","mill":"5"}}*'
                if light==2:
                    light_msg='{"type":"light","data":{"left":"green","front":"green","right":"green","mill":'+str(int(light_count/10+1))+'}}*'
                #红绿灯倒计时
                light_count=light_count-1
                s.send(light_msg.encode())

        #except queue.Empty:
        except Exception as e:
            # 没有消息在等待，我们要关闭掉。
            #print('  ', s.getpeername(), 'queue empty',file=sys.stderr)
            #inputs.remove(s)
            outputs.remove(s)
            print(e)
            print('connection close')
        else:
            #print('sending {!r} to {}'.format(next_msg,s.getpeername()),file=sys.stderr)
            #s.send(next_msg.encode())
            time.sleep(0.1)
            
    # 处理 「异常状况」
    '''
    for s in exceptional:
        #print('exception condition on', s.getpeername(),file=sys.stderr)
        # 停止监听此连接的输入。
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        # 移除此消息队列。
        #del message_queues[s]
    '''        
server.close()