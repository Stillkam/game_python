# -*- coding: utf-8 -*-
from sys import exit
from time import sleep
import pygame
from thread import *

black = (0,0,0)
red = (255,0,0)
slateGray = (112,128,105)
DarkSlateGra=(47,79,79)
DeepSkyBlue4=(0,104,139)
grey31=(79,79,79)
RoyalBlue=(65,105,225)
Grey=(190,190,190)

pygame.init()

xofont = pygame.font.SysFont("Century Schoolbook",48)
xo1render=xofont.render('x',1,black)

iforect=pygame.Rect(10,10,110,70)
p1rect=pygame.Rect(125,5,200,35)
p2rect=pygame.Rect(125,50,200,35)
ct2rect=pygame.Rect(350,10,150,60)

rect=[pygame.Rect(10,115,140,135)]
rect.append(pygame.Rect(175,115,140,135))
rect.append(pygame.Rect(340,115,140,135))
rect.append(pygame.Rect(10,275,140,135))
rect.append(pygame.Rect(175,275,140,135))
rect.append(pygame.Rect(340,275,140,135))
rect.append(pygame.Rect(10,440,140,135))
rect.append(pygame.Rect(175,440,140,135))
rect.append(pygame.Rect(340,440,140,135))

iforender=pygame.font.SysFont("arial",45).render(' vs',1,DarkSlateGra)
xo1render=pygame.font.SysFont("None",220).render('O',1,black)
xo2render=pygame.font.SysFont("None",220).render('O',1,black)

name=raw_input('Please input your PlayerName(English):\n')
host=raw_input('Please input the server ip:\n')
port=input('Please input the server port:\n')
import socket

while 1:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60*5)
    while 1:
        print 'connecting to '+host+':'+str(port)+'...\n'
        try:
            s.connect((host,port))
            if s.recv(1024)=='ok':
                print 'connected to the server!\n'
                break
        except:
            print 'connection fail!Please check the server ip!\n'
            #s.close()
            host=raw_input('Please input the server ip:\n')
            port=input('Please input the server port:\n')
    try:
        if s.recv(1024)=='ready':
            s.sendall(name)
    except socket.timeout:
        print 'connection timeout.'
        s.close()
        continue
    start=raw_input('Ready to Start the Game?(y/n)\n')
    if start=='n':
        s.close
        continue
    elif start=='y':
        pygame.font.init()
        screen = pygame.display.set_mode((500, 600))
        pygame.display.set_caption('MyGame')
        def drawscr(name,vs,use,color2):
            iforender=pygame.font.SysFont("arial",45).render(' vs',1,DarkSlateGra)
            p1font=pygame.font.SysFont("arial",25)
            p1render=p1font.render(name,1,DarkSlateGra)
            p2font=pygame.font.SysFont("arial",25)
            p2render=p2font.render(vs,1,DarkSlateGra)
            ct2font=pygame.font.SysFont("arial",40)
            ct2render=ct2font.render('Quit',1,DarkSlateGra)
            if use=='x':
                global xo1render
                xo1render=pygame.font.SysFont("None",220).render('X',1,black)
                global xo2render
                xo2render=pygame.font.SysFont("None",220).render('O',1,black)
            else:

                xo1render=pygame.font.SysFont("None",220).render('O',1,black)

                xo2render=pygame.font.SysFont("None",220).render('X',1,black)

            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, black, (10,256,480,15), 0)
            pygame.draw.rect(screen, black, (10,422,480,15), 0)
            pygame.draw.rect(screen, black, (156,110,15,480), 0)
            pygame.draw.rect(screen, black, (322,110,15,480), 0)
            pygame.draw.rect(screen,color2, (10,90,480,20), 0)
            pygame.draw.rect(screen, DeepSkyBlue4, (322,10,10,70), 0)
            pygame.draw.rect(screen,DarkSlateGra, (125,45,60,2), 0)

            screen.blit(iforender,iforect)
            screen.blit(p1render,p1rect)
            screen.blit(p2render,p2rect)
            screen.blit(ct2render,ct2rect)
            pygame.display.flip()

        def rcv():
            try:
                r=s.recv(59)
            except :
                print 'connection timeout.'
                s.close()
                return
            global recv
            recv=eval(r)
            if recv['type']=='2':
                global status1
                status1[int(recv['pos'])]=0
                screen.blit(xo2render,rect[int(recv['pos'])-1])
                pygame.display.update()

            elif recv['type']=='3':
                global stu
                status1[0]=0
                inf=''
                if recv['inf']=='1':
                    inf='WIN'
                elif recv['inf']=='2':
                    inf='LOSE'
                elif recv['inf']=='0':
                    inf='TIE'
                pygame.draw.rect(screen, (255,255,255), iforect, 0)
                iforender=pygame.font.SysFont("arial",45).render(inf,1,DarkSlateGra)
                screen.blit(iforender,iforect)
                pygame.display.update()
            stu[1]=0
        global status11
        status1=[1,1,1,1,1,1,1,1,1,1]
        global stu
        stu=[1,1]
        data={}
        global recv
        recv={}
        done = True
        def rcv1():
            try:
                r=s.recv(1024)
            except :
                print 'connection timeout.'
                s.close()
                return
            recv=eval(r)
            if recv['type']=='1' and recv['use']=='x':
                drawscr(name,recv['vs'],recv['use'],slateGray)
                status1=[1,1,1,1,1,1,1,1,1,1]
            if recv['type']=='1' and recv['use']=='o':
                drawscr(name,recv['vs'],recv['use'],red)

                status1=[1,1,1,1,1,1,1,1,1,1]
                try :
                    r=s.recv(1024)
                except socket.timeout:
                    print 'connection timeout.'
                    s.close()
                    return
                recv=eval(r)
                status1[int(recv['pos'])]=0
                screen.blit(xo2render,rect[int(recv['pos'])-1])
                pygame.display.update()
            stu[1]=0
        if stu[0]==1:
            stu[1]=1
            start_new_thread(rcv1,())
            stu[0]=0
        while done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done=False
            if stu[0]==1:
                stu[1]=1
                start_new_thread(rcv,())
                stu[0]=0
            mousexpos, mouseypos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]  and ct2rect.collidepoint(mousexpos, mouseypos):
                done=False
            elif pygame.mouse.get_pressed()[0]  and rect[0].collidepoint(mousexpos, mouseypos) and status1[1]  and status1[0] and not stu[1]:
                screen.blit(xo1render,rect[0])
                pygame.display.update()
                data['type']='2'
                data['pos']='1'
                s.sendall(str(data))
                stu[0]=1
            elif pygame.mouse.get_pressed()[0]  and rect[1].collidepoint(mousexpos, mouseypos) and status1[2] and status1[0] and   not stu[1]:
                screen.blit(xo1render,rect[1])
                pygame.display.update()
                data['type']='2'
                data['pos']='2'
                s.sendall(str(data))
                stu[0]=1
            elif pygame.mouse.get_pressed()[0]  and rect[2].collidepoint(mousexpos, mouseypos) and status1[3] and status1[0] and not stu[1]:
                screen.blit(xo1render,rect[2])
                pygame.display.update()
                data['type']='2'
                data['pos']='3'
                s.sendall(str(data))
                stu[0]=1
            elif pygame.mouse.get_pressed()[0]  and rect[3].collidepoint(mousexpos, mouseypos) and status1[4]  and status1[0] and not stu[1]:
                screen.blit(xo1render,rect[3])
                pygame.display.update()
                data['type']='2'
                data['pos']='4'
                s.sendall(str(data))
                stu[0]=1
            elif pygame.mouse.get_pressed()[0]  and rect[4].collidepoint(mousexpos, mouseypos) and status1[5]  and status1[0] and not stu[1]:
                screen.blit(xo1render,rect[4])
                pygame.display.update()
                data['type']='2'
                data['pos']='5'
                s.sendall(str(data))
                stu[0]=1
            elif pygame.mouse.get_pressed()[0]  and rect[5].collidepoint(mousexpos, mouseypos) and status1[6]  and status1[0] and not stu[1]:
                screen.blit(xo1render,rect[5])
                pygame.display.update()
                data['type']='2'
                data['pos']='6'
                s.sendall(str(data))
                stu[0]=1
            elif pygame.mouse.get_pressed()[0]  and rect[6].collidepoint(mousexpos, mouseypos) and status1[7]  and status1[0] and not stu[1]:
                screen.blit(xo1render,rect[6])
                pygame.display.update()
                data['type']='2'
                data['pos']='7'
                s.sendall(str(data))
                stu[0]=1
            elif pygame.mouse.get_pressed()[0]  and rect[7].collidepoint(mousexpos, mouseypos) and status1[8]  and status1[0] and not stu[1]:
                screen.blit(xo1render,rect[7])
                pygame.display.update()
                data['type']='2'
                data['pos']='8'
                s.sendall(str(data))
                stu[0]=1
            elif pygame.mouse.get_pressed()[0]  and rect[8].collidepoint(mousexpos, mouseypos) and status1[9]  and status1[0] and not stu[1]:
                screen.blit(xo1render,rect[8])
                pygame.display.update()
                data['type']='2'
                data['pos']='9'
                s.sendall(str(data))
                stu[0]=1
        pygame.quit()
        s.close()
    else:
        print "Sorry,I don't understand..."
        s.close()
        continue
