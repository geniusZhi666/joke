# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 14:42:04 2023

@author: Zhi
"""

import pandas as pd
import tkinter as tk
import imageio
import cv2
import numpy as np

top=tk.Tk() #窗口打开
top.geometry('620x480') #窗口大小设置
top.title('迷宫')#窗口标题设置
top["bg"]='white'#窗口背景色设置
menubar=tk.Menu(top)#菜单栏设置，如下，添加子菜单（添加对应功能）
top.iconbitmap('小和尚.ico')
filemenu=tk.Menu(menubar,tearoff=0)

filemenu.add_command(label='选择终点',command=lambda:menu00())
filemenu.add_separator()
filemenu.add_command(label='显示路线',command=lambda:menu01())
menubar.add_cascade(label='寻路',menu=filemenu)
top['menu']=menubar

img_gif = tk.PhotoImage(file = 'maze.gif')
label_img = tk.Label(top, image = img_gif)
label_img.place(x=0, y=0)

pre_route=list()    #宽度搜索得到的节点
q=list()    #队列结构控制循环次数
xx=[0,1,0,-1]   #右移、下移、左移、上移
yy=[1,0,-1,0]
visited=list()  #记录节点是否已遍历
father=list()   #每一个pre_route节点的父节点
route=list()


img_cv   = cv2.imread("maze.jpg")
img =  cv2.imread("maze.jpg",cv2.IMREAD_GRAYSCALE)
i_min=48
i_max=439
j_min=50
j_max=569
w=int((j_max-j_min+1)/8)
h=int((i_max-i_min+1)/8)
img_maze=[]
for i in range(h):
    img_h=[]
    for j in range(w):
        sum_ij=0
        for ii in range(8):
            for jj in range(8):
                sum_ij+=img[i_min+i*8+ii][j_min+j*8+jj]
        img_h.append(sum_ij)
    img_maze.append(img_h)
img_maze=np.array(img_maze)
cv_img=[["0" for j in range(w)] for i in range(h)]
for i in range(h):
    for j in range(w):
        if 10000> img_maze[i][j]>600:
            cv_img[i][j]="1"
l=[]
for i in range(h):
    rl=""
    for j in range(w):
        rl+=cv_img[i][j]
    l.append(rl)



# 导入图片
img = cv2.imread('maze.jpg')

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    
    # 点击鼠标左键
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 2, (255, 0, 0), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)
        global data 
        data= [x,y]
        
def find(xy):
    i_min=48
    i_max=439
    j_min=50
    j_max=569
    w=int((j_max-j_min+1)/8)
    h=int((i_max-i_min+1)/8)
    x=xy[1]
    y=xy[0]
    x_zd=0
    y_zd=0
    for i in range(i_min,i_max,8):
        if i<=x<i+8:
            x_zd=i
            break
    for j in range(j_min,j_max,8):
        if j<=y<j+8:
            y_zd=j
            break
    return [x_zd,y_zd]



def bfs(l,x,y,m,n):
    visited=[[0 for i in range(len(l[0]))]for j in range(len(l))]
    visited[x][y]=1 #入口节点设置为已遍历
    q.append([x,y])
    while q:    #队列为空则结束循环
        now=q[0]
        q.pop(0)    #移除队列头结点
        for i in range(4):
            point=[now[0]+xx[i],now[1]+yy[i]]   #当前节点
            if point[0]<0 or point[1]<0 or point[0]>=len(l) or point[1]>=len(l[0]) or visited[point[0]][point[1]]==1 or l[point[0]][point[1]]=='1':
                continue
            father.append(now)
            visited[point[0]][point[1]]=1
            q.append(point)
            pre_route.append(point)
            if point[0]==m and point[1]==n:
                print("success")
                return 1
    print("false")
    return 0

def get_route(father,pre_route):    #输出最短迷宫路径
    route=[pre_route[-1],father[-1]]
    for i in range(len(pre_route)-1,-1,-1):
        if pre_route[i]==route[-1]:
            route.append(father[i])
    route.reverse()
    print("迷宫最短路径为：\n",route)
    print("步长：",len(route)-1)
    return route

def gif_picture(route):
    img_gif0   = cv2.imread("maze.jpg")
    img_gif1=img_gif0.copy()
    print(route)
    frames = []
    for i in range(len(route)):
        
        img_gif  = img_gif0 .copy()
        for ii in range(8):
            for jj in range(8):
                img_gif[i_min+route[i][0]*8+ii][j_min+route[i][1]*8+jj]=img_gif0[400+ii][554+jj]
                img_gif1[i_min+route[i][0]*8+ii][j_min+route[i][1]*8+jj]=img_gif0[400+ii][554+jj]
        frames.append(img_gif)
    
    imageio.mimsave("route.gif", frames, 'GIF', duration = 0.1)
    cv2.imwrite('route_all.jpg', img_gif1)
    imageio.mimsave("route_all.gif", [img_gif1], 'GIF', duration = 0.1)
    
def menu00():
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    print(data)
    [x,y]=find(data)
    print([x,y])
    for i in range(8):
        for j in range(8):
            img[x+i][y+j]=img[400+i][554+j]+[0,0,200]
    gif_name = 'maze_new.gif'
    frames = []
    frames.append(img)
    # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.1)
    global img_gif1
    img_gif1 = tk.PhotoImage(file = 'maze_new.gif')
    global label_img
    label_img.configure(image=img_gif1)
        
    xx=44;yy=63
    m=(x-48)/8;n=(y-50)/8
    print(x,y)
    print(m,n)
    if bfs(l,xx,yy,m,n)==1:
        route=get_route(father,pre_route)
        gif_picture(route)      
    else:
        print("无解")
        tk.messagebox.showinfo(title='提示',message='无解')
        
def  menu01():
    global img_gif2
    img_gif2 = tk.PhotoImage(file = 'route_all.gif')
    global label_img
    label_img.configure(image=img_gif2)



top.mainloop()
