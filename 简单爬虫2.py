# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 21:07:16 2018

@author: 陈开锋
"""


from bs4 import BeautifulSoup
import requests
import time
import sys
import re
import itchat
from itchat.content import *
import threading

threads = []
UserList=[u'陈开锋',u'陈敏娟']
UserSetNum=[5,5]
UserSetState=[True,True]
User_Inf=[]
UserId=[]
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
}
urls = ["http://k3.icaile.com/","http://k3.icaile.com/ahk3.php","http://k3.icaile.com/gxk3.php","http://k3.icaile.com/hbk3.php","http://k3.icaile.com/hebk3.php","http://k3.icaile.com/gsk3.php","http://k3.icaile.com/shk3.php","http://k3.icaile.com/gzk3.php","http://k3.icaile.com/jlk3.php","http://k3.icaile.com/bjk3.php"]
shengfen=["江苏","安徽","广西","湖北","河北","甘肃","上海","贵州","吉林","北京"]
jishu=0
oushu=0
dashu=0
xiaoshu=0
UserNum = range(len(UserList))
ProvNum = range(len(shengfen))
dangriqihaoIinit=["000000000" for i in ProvNum]
dangriqihao=[["000000000" for i in ProvNum]for i in UserNum]


itchat.login()
itchat.auto_login()
friends_list = itchat.get_friends(update=True)
lock=threading.Lock()


def dangriqihao_init(indx):
    dangriqihaoIinit=["000000000" for i in ProvNum]
    print(dangriqihao[indx])
    dangriqihao[indx]=dangriqihaoIinit
    print(dangriqihao[indx])
    


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    global num_ac,num_ka,ka_flag,ac_flag,UserNum
    context_msg=msg.text
    if context_msg.isdigit():
        num=int(context_msg)
        for i in UserNum:
            if msg['User']['RemarkName']==UserList[i]:
                UserSetNum[i]=num
                lock.acquire()
                try:
                    dangriqihao_init(i)
                finally:
                    lock.release()
                ret_Message="%(UserName)s的连续次数设置为：%(cishu)d "%{'UserName':UserList[i],'cishu':num}
    else:
        if context_msg==u"关闭":
            for i in UserNum:
                if msg['User']['RemarkName']==UserList[i]:
                    UserSetState[i]= False
                    ret_Message="关闭%(UserName)s微信提醒成功"%{'UserName':UserList[i]}           
        elif context_msg==u"打开":
            for i in UserNum:
                if msg['User']['RemarkName']==UserList[i]:
                    UserSetState[i]= True
                    lock.acquire()
                    try:
                        dangriqihao_init(i)
                    finally:
                        lock.release()
                    ret_Message="%(UserName)s打开微信提醒成功"%{'UserName':UserList[i]} 
        else:
            ret_Message="请输入数字，连续次数默认为5"
    print(ret_Message)
    return ret_Message


def start_head():
    for i,names in enumerate(UserList):
        User_Inf.append(itchat.search_friends(name=names))
        UserId.append(User_Inf[i][0]["UserName"])
        itchat.send_msg("你的小可爱重启中····请稍后,连续期数默认为5,若要修改请自行设置", toUserName=UserId[i])

start_head()

def ichat_run():
    itchat.run()
    
        
def Scry_run():
    global jishu,oushu,dashu,xiaoshu,UserNum
    while 1:
        for index_i,url in enumerate(urls):
            attempts=0
            success=False
            while attempts<=5 and not success:
                try:
                    wb_data = requests.get(url,headers=headers,timeout=4)
                    success = True
                    print("重试次数",attempts)
                except Exception as e:
                    print("出现异常-->"+str(e))
                    attempts +=1
                    success=False
                    #print("正在尝试",attempts)
                    time.sleep(1)
            soup = BeautifulSoup(wb_data.text,'lxml')       
            qihao = soup.find_all("td",class_="chart-bg-qh")
            hezhi = soup.find_all("td",class_=re.compile("chart-bg-c6 blank-c6"),id=re.compile("a"))    
            for x,y in zip(qihao,hezhi):
                SUM_VAL=int(y.text)
                if SUM_VAL%2==0:
                    oushu=oushu+1
                    jishu=0
                else:
                    jishu=jishu+1;
                    oushu=0
                if SUM_VAL <=10:
                    xiaoshu=xiaoshu+1
                    dashu=0
                else:
                    dashu=dashu+1
                    xiaoshu=0
                    
                jioulianxu=(oushu if (oushu>jishu) else jishu)
                daxiaolianxu=(dashu if (dashu>xiaoshu) else xiaoshu)
                #print('期号:%s  和值:%d  奇偶连续期数:%d  大小连续期数:%d' %'x.text',y.text,jioulianxu,daxiaolianxu)
            for i in UserNum:
                print(UserList[i],UserSetNum[i],UserSetState[i])
                Text_Message="省份:%(shengfen)s 期号:%(qihao)s 和值:%(hezhi)d 奇偶连续期数:%(jioulianxu)d 大小连续期数:%(daxiaolianxu)d"%{'shengfen':shengfen[index_i],'qihao':x.text,'hezhi':SUM_VAL,'jioulianxu':jioulianxu,'daxiaolianxu':daxiaolianxu}
                print(Text_Message)
                if x.text != dangriqihao[i][index_i]:
                    lock.acquire()
                    try:
                        dangriqihao[i][index_i]=x.text
                    finally:
                        lock.release()
                    #Text_Message="省份:%(shengfen)s 期号:%(qihao)s 和值:%(hezhi)d 奇偶连续期数:%(jioulianxu)d 大小连续期数:%(daxiaolianxu)d"%{'shengfen':shengfen[index_i],'qihao':x.text,'hezhi':SUM_VAL,'jioulianxu':jioulianxu,'daxiaolianxu':daxiaolianxu}
                    if UserSetState[i]== True:
                        if jioulianxu>=UserSetNum[i] or daxiaolianxu>=UserSetNum[i]:
                            print(UserSetNum[i],Text_Message)
                            itchat.send_msg(Text_Message, toUserName=UserId[i])
            print(shengfen[index_i]+"已过！")
            #time.sleep(1)
            if index_i==9:
                index_i=0
            #time.sleep(10)
            #itchat.logout() 
        time.sleep(5)
    #print(haoma)
FunList=[Scry_run,ichat_run]
files = range(len(FunList))
for i in files:
    t = threading.Thread(target=FunList[i],args=())
    threads.append(t)
for i in files:
    threads[i].start()
for i in files:
    threads[i].join()

