import itchat
import time
import urllib.request
import json
import requests
from itchat.content import *
from requests_html import HTMLSession


url_tuling="http://www.tuling123.com/openapi/api"
tuling_key="f9edc634f48e406bb2d6d30132ff8293"

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_single_reply(msg):
    # cont = alice.respond(msg['Text'])
    print(msg["Content"])
    data_json={
        "key":tuling_key,
        "info":msg["Content"]
    }
    if "快递" in msg["Content"]:
        data_json["userid"]="3904620736244"
    if '吃什么' in msg["Content"]:
        itchat.send('小西云回复：{}'.format('可选有：豆腐、土豆、黄瓜、蒜苗'), msg['FromUserName'])
    else:
        pass
        # # cont = requests.get('http://www.tuling123.com/openapi/api?key=f9edc634f48e406bb2d6d30132ff8293&info=%s' % msg['Content']).content
        # cont=requests.post(url=url_tuling,json=data_json).content
        # m = json.loads(cont)
        # time.sleep(1)
        #
        # itchat.send('小西云回复：{}'.format(m['text']), msg['FromUserName'])
        # if m['code'] == 200000:
        #     itchat.send(m['url'], msg['FromUserName'])
        # if m['code'] == 302000:
        #     itchat.send(m['list'], msg['FromUserName'])
        # if m['code'] == 308000:
        #     itchat.send(m['list'], msg['FromUserName'])


@itchat.msg_register(TEXT, isGroupChat = True)
def text_reply(msg):
    # for (k,v) in msg.items():
    #     print(k,v)
    data_json={
        "key":tuling_key,
        "info":msg["Content"]
    }
    cont = requests.post(url=url_tuling, json=data_json).content
    m = json.loads(cont)
    print(m)
    time.sleep(1.5)
    talk_show = []
    talk_show += [get_chatroom_username(u'信计'), get_chatroom_username(u'朱家群'), get_chatroom_username(u'上山打老虎'),get_chatroom_username(u'么么哒。💋')]
    #print(msg['FromUserName'])#msg['IsAt'] or
    if  msg['FromUserName'] in talk_show:
    #if msg['FromUserName'] in talk_show:
        if msg['Content']=='':
            itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], "- -@"), msg['FromUserName'])
        if '你是谁' in msg['Content']:
            itchat.send('小西云回复：我是小西云', msg['FromUserName'])
        else:
            itchat.send('小西云回复：{}'.format(m['text']), msg['FromUserName'])
        if m['code'] == 200000:
            itchat.send(m['url'], msg['FromUserName'])
        if m['code'] == 302000:
            itchat.send(m['list'], msg['FromUserName'])
        if m['code'] == 308000:
            itchat.send(m['list'], msg['FromUserName'])

all_firends=itchat.get_friends()[1:]
def find_firend_user_name_by_nick_name(firends_list,wechat_nick_name):
    user_name='UserName'
    nick_name='NickName'
    _get_list=[]
    for x in firends_list:
        if wechat_nick_name in x[nick_name]:
            _get_list.append(x)
    print(_get_list)
    return _get_list

def get_chatroom_username(room_name):
    try:
        chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return


def send_message_to_nick_name(wechat_nick_name):
    UserList=find_firend_user_name_by_nick_name(all_firends,wechat_nick_name)
    for _u in UserList:
        itchat.send("Hello {}! 你可以找我聊天。查询天气、快递等，如：发送 桂林天气 给我。".format(_u.NickName),toUserName=_u.UserName)
        print('message sended')

def get_news():
    time_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    msg = '{}资讯:\n'.format(time_now)
    s=HTMLSession()
    r=s.get('http://news.baidu.com/finance')
    sets=r.html.find('#col_focus > div.l-middle-col > div',first=True)
    ass=sets.find('a')
    n=1
    for a in ass:
        msg+=''.join('{}、{}\n'.format(n,a.text))
        n+=1
    return msg
# send_message_to_nick_name("Monica")

itchat.auto_login(hotReload=True)
itchat.send(get_news(),get_chatroom_username(u'经济研讨'))
itchat.run()