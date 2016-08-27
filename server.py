# -*- coding: utf-8 -*-

import socket
import sys
from thread import *

def win(pos):
    if len(pos)<3:
        return 0
    else:
        if pos.count('1'):
            if pos.count('4') and pos.count('7') or pos.count('2') and pos.count('3'):
                return 1
        if pos.count('5'):
            if pos.count('4') and pos.count('6') or pos.count('2') and pos.count('8') or pos.count('1') and pos.count('9') or pos.count('3') and pos.count('7'):
                return 1
        if pos.count('9'):
            if pos.count('7') and pos.count('8') or pos.count('3') and pos.count('6'):
                return 1
        return 0


HOST = ''
PORT = 6666
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

def client_vs(conn1,conn2,addr1,addr2):
    pos1=[]
    pos2=[]
    conn1.settimeout(60*5)
    conn2.settimeout(60*5)
    try:
        conn1.sendall('ready')
        conn2.sendall('ready')
    except:
        print 'Connection between '+addr1+' and '+addr2+' timeout.'
        conn1.close()
        conn2.close()
    try:
        name1 = conn1.recv(1024)
        name2 = conn2.recv(1024)
        print name1+' vs '+name2
    except socket.timeout:
        print 'Connection between '+addr1+' and '+addr2+' timeout.'
        conn1.close()
        conn2.close()
        return
    data1={'type':'1','vs':'','use':'x','pos':'','inf':'0'}
    data1['vs']=name2
    conn1.sendall(str(data1))
    data1['vs']=''
    data2={'type':'1','vs':'','use':'o','pos':'','inf':'0'}
    data2['vs']=name1
    conn2.sendall(str(data2))
    data2['vs']=''
    turn=1
    while True:
        if turn==1:
            try:
                r=conn1.recv(1024)
            except:
                print 'connection to '+addr1+'timeout\n'
                conn1.close()
                conn2.close()
                break
            recv1=eval(r)
            turn=2
            if recv1['type']=='2':
                data2['type']='2'
                data2['pos']=recv1['pos']
                try:
                    conn2.sendall(str(data2))
                except:
                    print 'connection to '+addr2+'timeout\n'
                    conn1.close()
                    conn2.close()
                    break
                pos1.append(recv1['pos'])
                if win(pos1):
                    data1['type']='3'
                    data1['inf']='1'
                    data2['type']='3'
                    data2['inf']='2'
                    conn1.sendall(str(data1))
                    conn2.sendall(str(data2))
                    break
                elif len(pos1)=='5':
                    data1['type']='3'
                    data1['inf']='0'
                    data2['type']='3'
                    data2['inf']='0'
                    conn1.sendall(str(data1))

                    conn2.sendall(str(data2))
                    break
        if turn==2:
            try:
                r=conn2.recv(1024)
            except :
                print 'connection timeout\n'
                conn1.close()
                conn2.close()
                break
            recv2=eval(r)
            turn=1
            if recv2['type']=='2':
                data1['type']='2'
                data1['pos']=recv2['pos']
                try:
                    conn1.sendall(str(data1))
                except:
                    print 'connection to '+addr1+'timeout\n'
                    conn1.close()
                    conn2.close()
                    break
                pos2.append(recv2['pos'])
                if win(pos2):
                    data2['type']='3'
                    data2['inf']='1'
                    data1['type']='3'
                    data1['inf']='2'
                    conn1.sendall(str(data1))
                    conn2.sendall(str(data2))
                    break
                elif len(pos2)=='5':
                    data1['type']='3'
                    data1['inf']='0'
                    data2['type']='3'
                    data2['inf']='0'
                    conn1.sendall(str(data1))
                    conn2.sendall(str(data2))
                    break
while 1:
    conn1, addr1 = s.accept()
    conn1.sendall('ok')
    print 'Connected with ' + addr1[0] + ':' + str(addr1[1])
    conn2, addr2 = s.accept()
    conn2.sendall('ok')
    print 'Connected with ' + addr2[0] + ':' + str(addr2[1])
    start_new_thread(client_vs ,(conn1,conn2,addr1[0],addr2[0]))
s.close()
