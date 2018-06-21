# -*- coding: utf-8 -*-
# @Project : upupup 
# @Time    : 2018/6/15 14:06
# @Author  : 
# @File    : PyNews.py
# @Software: PyCharm Community Edition

import itchat
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import ttk
import os
import math
import threading
from tkinter import messagebox
from ChatNews import get_news,get_chatroom_username

class ChatPy():
    def __init__(self):
        self.img_path = 'imgs'
        self.res_path='resources'
        self.iconico='bitbug_favicon.ico'
        self.current_user_logo_name= 'user_logo.jpg'
        self.default_user_log='moren.jpg'
        self.bg_image_name='bg.png'
        self.root = tk.Tk()
        self.root.title(u'微信助手')
        self.root.iconbitmap('{}/{}'.format(self.res_path,self.iconico))
        self.root.geometry('800x600')
        self.gui_grid()
        self.run_gui()
    def login_web(self):
        t1 = threading.Thread(target=self.login_web_thread)
        t1.start()
    def login_web_thread(self):
        self.login_button.config(state='disable')
        try:
            itchat.auto_login()
        except Exception as e:
            print(e)
            self.login_button.config(state='normal')
            return
        self.user_name_value_lable.config(
            text=self.get_myself_info()['NickName'],
            fg='blue',
            font=('黑体',12)
        )
        self.get_self_head_img()
        self.user_logo = self.get_head_img_50x50(self.img_path, self.current_user_logo_name)
        self.head_image_lable.config(image=self.user_logo)
        self.mix_logo_button.config(state='normal')
        self.login_button.config(state='disable',text='已登录')
        self.login_out_button.config(state='normal')
        self.show_firends()
    def login_out(self):
        itchat.logout()
        self.user_name_value_lable.config(text=u'已退出',font=('黑体',10))
        self.login_button.config(state='normal', text='登录')
    def mix_logo(self):
        pass
    #     self.mix_logo_button.config(text=u'请稍等...', state='disable')
    #     t1 = threading.Thread(target=self.get_head_image)
    #     t1.start()
    def get_firends_list(self)->list:
        return itchat.get_friends()
    def get_myself_info(self)->list:
        return self.get_firends_list()[0]
    def get_all_firends_list(self)->list:
        return self.get_firends_list()[1:]
    def get_head_img_50x50(self,res_path,image_name)->ImageTk.PhotoImage:
        head_img_pil=Image.open('{}/{}'.format(res_path,image_name))
        return ImageTk.PhotoImage(head_img_pil.resize((50,50)))
    def get_res_image(self,res_path,image_name,im_size_x,im_size_y)->ImageTk.PhotoImage:
        head_img_pil = Image.open('{}/{}'.format(res_path, image_name))
        return ImageTk.PhotoImage(head_img_pil.resize((im_size_x, im_size_y)))
    def get_self_head_img(self) ->None:
        im=itchat.get_head_img(self.get_myself_info()["UserName"])
        with open('{}/{}'.format(self.img_path, self.current_user_logo_name), 'wb') as fp:
            fp.write(im)
            fp.close()
    #功能函数
    def send_news(self):
        itchat.send(get_news(), get_chatroom_username(u'经济研讨'))
    def show_firends(self):
        firends_all_list=self.get_all_firends_list()
        for frd in firends_all_list:
            sex='其他'
            if frd['Sex']==2:
                sex='女'
            if frd['Sex']==1:
                sex='男'
            frd_div=(frd['UserName'],frd['NickName'],frd['RemarkName'],sex)
            print(frd_div)
            try:
                self.firends_tree.insert('','end',values=frd_div[1:])
            except Exception as e:
                nick_name=frd['NickName'].encode('utf8')
                frd_div = (frd['UserName'],nick_name, frd['RemarkName'], sex)
                self.firends_tree.insert('', 'end', values=frd_div[1:])
                print(e)

    def gui_grid(self):
        #login_frame
        self.lab_bg = self.get_res_image(self.res_path, self.bg_image_name, 300, 100)
        login_frame=tk.LabelFrame(
            self.root,
            width=300,
            height=100,
            relief='groove'
        )
        bg_label=tk.Label(login_frame,image=self.lab_bg)
        user_name_lable = tk.Label(
            login_frame,
            text=u'您好：',
            fg='gray',
            font=('黑体','12')
        )
        self.default_image=self.get_head_img_50x50(self.res_path,self.default_user_log)
        self.head_image_lable=tk.Label(
            login_frame,
            image=self.default_image,
            relief='raised'
        )
        self.user_name_value_lable=tk.Label(
            login_frame,
            text=u'请扫码登录'
        )
        self.mix_logo_button=tk.Button(
            login_frame,
            state='disable',
            text=u'生成拼图',
            command=self.mix_logo
        )
        self.login_button=tk.Button(
            login_frame,
            text=u'登录',
            command=self.login_web
        )
        self.login_out_button=tk.Button(
            login_frame,
            text=u'退出',
            state='disable',
            command=self.login_out
        )
        self.send_new_button=tk.Button(
            login_frame,
            text=u'发新闻',
            command=self.send_news
        )
        #好友列表 firends_frame
        firends_frame = tk.LabelFrame(
            self.root,
            width=300,
            height=500,
            relief='groove',
            bg='#CCCCCC'
        )
        self.firends_tree=ttk.Treeview(firends_frame,show='headings')
        scroll=tk.Scrollbar(firends_frame)
        self.firends_tree['height']=22
        self.firends_tree['yscrollcommand']=scroll.set
        scroll['command']=self.firends_tree.yview
        cl1='nickname'
        cl2= 'nicknick'
        cl3='sex'
        self.firends_tree['columns'] = [cl1,cl2,cl3 ]
        self.firends_tree.column(cl1, width=70)
        self.firends_tree.column(cl2, width=70)
        self.firends_tree.column(cl3, width=70)
        self.firends_tree.heading(cl1, text='昵称')
        self.firends_tree.heading(cl2, text='备注名')
        self.firends_tree.heading(cl3, text='性别')
        #ui grid
        #frame grid
        login_frame.grid(row=0, column=0,sticky=tk.W,padx=5, pady=5)
        firends_frame.grid(row=1,column=0)
        #login_frame
        bg_label.place(x=0,y=0)
        user_name_lable.place(x=0, y=0)
        self.user_name_value_lable.place(x=52, y=40)
        # self.mix_logo_button.place(x=175, y=0,width=60,height=20)
        self.login_button.place(x=255, y=0,width=40, height=20)
        self.head_image_lable.place(x=0,y=40,width=50,height=50)
        self.login_out_button.place(x=255, y=20,width=40, height=20)
        self.send_new_button.place(x=255, y=40,width=40, height=20)
        #firends_frame
        self.firends_tree.place(x=0,y=0,width=270)
        scroll.place(x=270,y=0,height=466)

    def close_window(self):
        # messagebox.showinfo('info','window close')
        try:
            itchat.logout()
        except Exception as e:
            pass
        self.root.destroy()
    def run_gui(self):
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        self.root.mainloop()

if __name__=="__main__":
    a=ChatPy()