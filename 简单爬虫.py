# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 21:07:16 2018

@author: 陈开锋
"""


from bs4 import BeautifulSoup
import requests
import time
import sys

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
}
url = "https://kuai3.cjcp.com.cn/jiangsu/kaijiang/"

wb_data = requests.get(url,headers=headers)

#所有返回的报文
soup = BeautifulSoup(wb_data.text,'lxml')

#contex = soup.find_all("td",class_="kjjg_hm_bg")
#contex = soup.find_all("tr")
#selector=etree.HTML(wb_data)
#title=soup.title
#筛选出该标签下的报文 总的期数
qishu_count = soup.select("table.kjjg_table tr ")

jishu=0
oushu=0

while 1:
    for index,qishu in enumerate(qishu_count):
    #print(qishu)
        if index==0:
            continue
    #print(qishu_count[index])
        meiqi="".join('%s'%id for id in qishu_count[index])
        meiqi_context = BeautifulSoup(meiqi,'lxml')
        meiqi_context_td = meiqi_context.find_all('td')
        for index2,qishu_meitiao in enumerate(meiqi_context_td):
            if index2==0:
                title=meiqi_context_td[0].text
            if index2==1:
                time_val=meiqi_context_td[1].text
            if index2==2:
                nums="".join('%s'%id2 for id2 in qishu_meitiao)
                nums = BeautifulSoup(nums,'lxml')
                num = nums.find_all('div')
                num1=num[1].text
                num2=num[2].text
                num3=num[3].text
            if index2==3:
                sum_val=meiqi_context_td[3].text
        sum_val_i=int(sum_val)
        if index==1:
            if sum_val_i%2 ==0:
                oushu=1
            else:
                jishu=1
        else:
            if oushu==1:
                if sum_val_i%2==0:
                    lianxu=lianxu+1
                else:
                    lianxu=0
            else:
                if sum_val_i%2==1:
                    lianxu=lianxu+1
                else:
                    lianx=0
        
        lianxu=(oushu if (oushu>jishu) else jishu)
        print(title,time_val,num1,num2,num2,sum_val,lianxu)
    time.sleep(1*60*10)
    
    
'''
for index,qishu in enumerate(qishu_count):
    #print(qishu)
    if index==0:
        continue
    #print(qishu_count[index])
    meiqi="".join('%s'%id for id in qishu_count[index])
    meiqi_context = BeautifulSoup(meiqi,'lxml')
    meiqi_context_td = meiqi_context.find_all('td')
    for index2,qishu_meitiao in enumerate(meiqi_context_td):
        if index2==0:
            title=meiqi_context_td[0].text
        if index2==1:
            time_val=meiqi_context_td[1].text
        if index2==2:
            nums="".join('%s'%id2 for id2 in qishu_meitiao)
            nums = BeautifulSoup(nums,'lxml')
            num = nums.find_all('div')
            num1=num[1].text
            num2=num[2].text
            num3=num[3].text
        if index2==3:
            sum_val=meiqi_context_td[3].text
    sum_val_i=int(sum_val)
    if index==1:
        if sum_val_i%2 ==0:
            oushu=1
        else:
            jishu=1
    else:
        if oushu==1:
            if sum_val_i%2==0:
                lianxu=lianxu+1
            else:
                lianxu=0
        else:
            if sum_val_i%2==1:
                lianxu=lianxu+1
            else:
                lianx=0
        
    lianxu=(oushu if (oushu>jishu) else jishu)
    print(title,time_val,num1,num2,num2,sum_val,lianxu)
'''

#print(soup2)
#soup2 = BeautifulSoup(qishu[2],'lxml')
#print(wb_data.text)
#print(soup.title.string.rstrip())
#print(soup.title.parent.name)

#print(soup2.body.td.text)
'''
for i in qishu:
    if i==2:
        nums="".join('%s'%id for id in qishu[i])
        nums = BeautifulSoup(nums,'lxml')
        num = nums.find_all('td')
        num1=num[1]
        num2=num[2]
        num3=num[3]
'''
#print()
#print()
#print()
#print()
#print()
#print()
#print()
#print()
#print()
#print()
#print()
#print()
#print()
#print()



'''
for hmbg in hmbgs:
    print(hmbg)
    
'''