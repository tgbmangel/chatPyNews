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
import time
import threading
from tkinter import messagebox
import unicodedata

class ChatPy():
    def __init__(self):
        self.img_path = 'imgs'
        self.res_path='resources'
        self.iconico='bitbug_favicon.ico'
        self.current_user_logo_name= 'user_logo.jpg'
        self.default_user_log='moren.jpg'
        self.bg_image_name='bg.png'
        self.tip_img_name='tongxun.jpg'
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
            # itchat.auto_login(hotReload=True)
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
        self.deltree(self.send_firends_tree)
        self.show_firends()
        self.show_chatrooms()
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
    def get_chat_rooms(self):
        return itchat.get_chatrooms()
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
    def send_ad_message(self,treeview,message,send_button,to_chat_room):
        send_button.config(state='disable')
        if to_chat_room:
            item_list=treeview.selection()
        else:
            item_list=treeview.get_children()
        for item in item_list:
            time.sleep(1.5)
            item_text=treeview.item(item,'values')
            if item_text:
                itchat.send(message,toUserName=item_text[0])
            else:
                print('no send list')
        send_button.config(state='normal')
    #功能函数
    def send_ad_to_firends(self):
        print('send ad click')
        ad_text=self.ad_text_entry.get('1.0',tk.END)
        if ad_text.strip():
            send_meassage_thread= threading.Thread(target=self.send_ad_message,args=(self.send_firends_tree,ad_text,self.send_message_button,False,))
            send_meassage_thread.start()
        else:
            messagebox.showinfo('提示', '请输入信息内容')
            print('ad text null')
    def send_ad_to_chat_room(self):
        print('send ad chatroom click')
        ad_text=self.ad_text_entry.get('1.0',tk.END)
        if ad_text.strip():

            send_meassage_thread= threading.Thread(target=self.send_ad_message,args=(self.qun_list_tree,ad_text,self.send_chat_room_button,True,))
            send_meassage_thread.start()
        else:
            messagebox.showinfo('提示', '请输入信息内容')
            print('ad text null')
    def unicode_nickname(self,input_string):
        print(input_string)
        strrr=ascii(input_string)
        b=''
        if 'U000' in strrr:
            str_list = strrr.split('\'')[1].split('\\')
            for x in str_list:
                print(x)
                if 'U000' in x:
                    pass
                elif not x:
                    pass
                else:
                    a = '\\{}'.format(x)
                    b=b+a
            final_str=b.encode('utf-8').decode('unicode_escape')
            return final_str
        else:
            return input_string

    def show_firends(self):
        firends_all_list=self.get_all_firends_list()
        self.deltree(self.firends_tree)
        for frd in firends_all_list:
            sex='其他'
            if frd['Sex']==2:
                sex='女'
            if frd['Sex']==1:
                sex='男'
            frd_div=(frd['UserName'],frd['NickName'],frd['RemarkName'],sex)
            print(frd_div)
            # self.firends_tree.insert('', 'end', values=frd_div)
            try:
                self.firends_tree.insert('','end',values=frd_div)
            except tk._tkinter.TclError:
                nick_name=self.unicode_nickname(frd['NickName'])
                remark_name=self.unicode_nickname(frd['RemarkName'])
                frd_div = (frd['UserName'],nick_name,remark_name, sex)
                self.firends_tree.insert('', 'end', values=frd_div)
            except Exception as e:
                print(e)
        self.firends_number_label.config(text='好友数：{}'.format(len(self.firends_tree.get_children())))
    def show_chatrooms(self):
        '''
        展示群列表
        :return:
        '''
        chat_rooms_list=self.get_chat_rooms()
        self.deltree(self.qun_list_tree)
        for chtroom in chat_rooms_list:
            chat_rooom=chtroom['UserName'],chtroom['NickName']
            try:
                self.qun_list_tree.insert('', 'end', values=chat_rooom)
            except tk._tkinter.TclError:
                nick_name = self.unicode_nickname(chtroom['NickName'])
                chat_rooom = (chtroom['UserName'], nick_name)
                self.qun_list_tree.insert('', 'end', values=chat_rooom)
            except Exception as e:
                print(e)

    def deltree(self,tree_view):
        '''
        清空treeview
        :param tree_view:
        :return:
        '''
        x = tree_view.get_children()
        for item in x:
            tree_view.delete(item)

    def check_repeat(self,tree_view,item_text_tuple):
        '''
        目前存在bug，无法正确判断是否存在
        :param tree_view:
        :param item_text_tuple:
        :return:
        '''
        if_not_in=True
        for item in tree_view.get_children():
            item_text = tree_view.item(item, "values")
            if item_text_tuple[0]==item_text[0]:
                if_not_in= False
        if if_not_in:
            tree_view.insert('', 'end', values=item_text_tuple)
    def del_from_send_firend_list_tree(self,event):
        '''
        双击事件
        :param event:
        :return:
        '''
        print('双击')
        for item in self.send_firends_tree.selection():
            self.send_firends_tree.delete(item)

    def select_send_firends(self,event):
        '''
        单机事件,firend_tree
        :param event:
        :return:
        '''
        print('单击')
        for item in self.firends_tree.selection():
            item_text_firends = self.firends_tree.item(item, "values")
            print(item_text_firends)
            self.check_repeat(self.send_firends_tree,item_text_firends)
    # def select_chat_room(self,event):
    #     '''
    #     群列表，单机多选 qun_list_tree
    #     :param event:
    #     :return:
    #     '''
    #     for item in self.qun_list_tree.selection():
    #         item_text_chat_room = self.qun_list_tree.item(item, "values")
    #         print(item_text_chat_room)
    ###################################################
    #UI
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
        # self.send_new_button=tk.Button(
        #     login_frame,
        #     text=u'发新闻',
        #     command=self.send_news
        # )
        #######################################################
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
        cl0='username'
        cl1='nickname'
        cl2= 'nicknick'
        cl3='sex'
        self.firends_tree['columns'] = [cl0,cl1,cl2,cl3 ]
        self.firends_tree.column(cl0, width=30)
        self.firends_tree.column(cl1, width=70)
        self.firends_tree.column(cl2, width=70)
        self.firends_tree.column(cl3, width=30)
        self.firends_tree.heading(cl0, text='user')
        self.firends_tree.heading(cl1, text='昵称')
        self.firends_tree.heading(cl2, text='备注名')
        self.firends_tree.heading(cl3, text='性别')
        self.firends_number_label=tk.Label(
            firends_frame,
            text='好友数：'
        )
        self.firends_fresh_button=tk.Button(
            firends_frame,
            text='f',
            command=self.show_firends
        )
        #######################################################
        #send_list_frame
        send_firends_frame = tk.LabelFrame(
            self.root,
            width=480,
            height=300,
            relief='groove',
            bg='#DEDEDE'
        )
        #treeview send_firends_tree
        self.send_firends_tree=ttk.Treeview(send_firends_frame,show='headings')
        send_scroll=tk.Scrollbar(send_firends_frame)
        self.send_firends_tree['height']=12
        self.send_firends_tree['yscrollcommand']=send_scroll.set
        send_scroll['command']=self.send_firends_tree.yview
        cl0='username'
        cl1='nickname'
        cl2= 'nicknick'
        cl3='sex'
        self.send_firends_tree['columns'] = [cl0,cl1,cl2,cl3 ]
        self.send_firends_tree.column(cl0, width=30)
        self.send_firends_tree.column(cl1, width=70)
        self.send_firends_tree.column(cl2, width=70)
        self.send_firends_tree.column(cl3, width=30)
        self.send_firends_tree.heading(cl0, text='user')
        self.send_firends_tree.heading(cl1, text='昵称')
        self.send_firends_tree.heading(cl2, text='备注名')
        self.send_firends_tree.heading(cl3, text='性别')
        #labels
        send_list_label=tk.Label(
            send_firends_frame,
            text='待发送好友列表(双击名称取消):'
        )
        ad_label=tk.Label(
            send_firends_frame,
            text='发送内容:'
        )
        #广告文本
        self.ad_text_entry=tk.Text(
            send_firends_frame,
            height=14,
            width=24
        )
        #send button
        self.send_message_button=tk.Button(
            send_firends_frame,
            text=u'发广告',
            command=self.send_ad_to_firends
        )
        del_button=tk.Button(
            send_firends_frame,
            text=u'清空发送列表',
            command=lambda :self.deltree(tree_view=self.send_firends_tree)
        )
        #######################################################
        #qun_frame
        qun_frame= tk.LabelFrame(
            self.root,
            width=480,
            height=180,
            relief='groove',
            bg='#DEDEDE'
        )
        #qun_list_tree
        col0='username'
        col1='name'
        self.qun_list_tree=ttk.Treeview(qun_frame,show='headings',columns=(col0,col1))
        self.qun_list_tree['selectmode']='extended'
        self.qun_list_tree['height']=6
        self.qun_list_tree.column(col0, width=10)
        self.qun_list_tree.column(col1, width=70)
        self.qun_list_tree.heading(col0, text='username')
        self.qun_list_tree.heading(col1, text='已有微信群')
        qun_scroll = tk.Scrollbar(qun_frame)
        self.qun_list_tree['yscrollcommand']=qun_scroll.set
        qun_scroll['command']=self.qun_list_tree.yview
        #labels
        qun_label=tk.Label(
            qun_frame,
            text='群列表,按【Ctrl】进行多选:'
        )
        self.tip_image=self.get_res_image(self.res_path,self.tip_img_name,200,100)

        img_tip_label=tk.Label(
            qun_frame,
            image=self.tip_image
        )
        #send_chat_room_button
        self.fresh_chatrooms_button=tk.Button(
            qun_frame,
            text='刷新群',
            command=self.show_chatrooms
        )
        self.send_chat_room_button=tk.Button(
            qun_frame,
            text='发到群',
            command=self.send_ad_to_chat_room
        )
        #######################################################
        #ui grid
        #frame grid
        login_frame.grid(row=0, column=0,sticky=tk.W,padx=5, pady=5)
        firends_frame.grid(row=1,column=0,rowspan=2)
        send_firends_frame.grid(row=1,column=1,sticky=tk.N)
        qun_frame.grid(row=2,column=1,sticky=tk.N)
        #login_frame
        bg_label.place(x=0,y=0)
        user_name_lable.place(x=0, y=0)
        self.user_name_value_lable.place(x=52, y=40)
        # self.mix_logo_button.place(x=175, y=0,width=60,height=20)
        self.login_button.place(x=255, y=0,width=40, height=20)
        self.head_image_lable.place(x=0,y=40,width=50,height=50)
        self.login_out_button.place(x=255, y=20,width=40, height=20)
        # self.send_new_button.place(x=255, y=40,width=40, height=20)
        #firends_frame
        self.firends_tree.place(x=0,y=0,width=270)
        scroll.place(x=270,y=0,height=466)
        self.firends_number_label.place(x=0,y=466)
        self.firends_fresh_button.place(x=50,y=466)
        #send_list_frame
        send_list_label.place(x=0,y=0)
        ad_label.place(x=290,y=0)
        self.send_firends_tree.place(x=0,y=24,width=270)
        send_scroll.place(x=270,y=24,height=267)
        self.ad_text_entry.place(x=290,y=24)
        self.send_message_button.place(x=290,y=220)
        del_button.place(x=290,y=260)
        #qun_frame
        self.qun_list_tree.place(x=0,y=24,width=270)
        qun_scroll.place(x=270, y=24, height=145)
        qun_label.place(x=0,y=0)
        img_tip_label.place(x=290,y=24)
        self.send_chat_room_button.place(x=290,y=140)
        self.fresh_chatrooms_button.place(x=350, y=140)
        #######################################################
    def close_window(self):
        # messagebox.showinfo('info','window close')
        try:
            itchat.logout()
            pass
        except Exception as e:
            pass
        self.root.destroy()
    def run_gui(self):
        #######################################################
        #事件绑定
        self.firends_tree.bind('<ButtonRelease-1>', self.select_send_firends)
        # self.qun_list_tree.bind('<Leave>', self.select_chat_room)
        self.send_firends_tree.bind('<Double-Button-1>', self.del_from_send_firend_list_tree)
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        #######################################################
        #主界面
        self.root.mainloop()

if __name__=="__main__":
    start=ChatPy()