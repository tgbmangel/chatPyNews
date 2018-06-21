# -*- coding: utf-8 -*-
# @Project : P3 
# @Time    : 2018/6/11 10:00
# @Author  : 
# @File    : ChatNews.py
# @Software: PyCharm Community Edition
import time
from requests_html import HTMLSession
import itchat

def get_news():
    time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    msg = '{}，来自百度财经:\n'.format(time_now)
    s=HTMLSession()
    r=s.get('http://news.baidu.com/finance')
    sets=r.html.find('#col_focus > div.l-middle-col > div',first=True)
    ass=sets.find('a')
    n=1
    for a in ass:
        msg+=''.join('{}、{}\n'.format(n,a.text))
        n+=1
    return msg


def get_chatroom_username(room_name):
    try:
        chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return

def get_chat_rooms_all(update=False, contactOnly=True):
    try:
        rooms_list=itchat.get_chatrooms()
        for r in rooms_list:
            print(r)
    except Exception as e:
        print(e)

if __name__=="__main__":
    itchat.auto_login(hotReload=True)
    get_chat_rooms_all()