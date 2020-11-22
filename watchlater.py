import requests
import feedparser
import json
from time import mktime
from datetime import datetime
import time

def getRSS():
    
    listHourLag = []
    listMinsLag = []
    listAVNum = []

    with open('D:/python_practice/bilibiliWatchlater/info.json', 'r') as myfile:
        data = myfile.read()

    obj = json.loads(data)
    url = str(obj['URL'])

    rss = feedparser.parse(url)
    

    print(rss.feed.title)
    print("\n")
    # print(rss.entries[0].id)
    # print(rss.entries[0].link)
    # print(rss.entries[0].title)
    # print(rss.entries[0].author)
    # print(rss.entries[0].description)


    for i in rss['entries']:
        print("id:"+" "+i['id'])
        print("link:"+" "+i['link'])
        print("title:"+" "+i['title'])
        print("author:"+" "+i['author'])
        print("description:"+" "+i['description'])
        print(i.updated_parsed)
        # print(type(i.updated_parsed[3]))
        # timediff = datetime.now() - datetime.fromtimestamp()
        publishHour = i.updated_parsed[3] + 8
        nowHour = time.localtime()[3]
        nowMin = time.localtime()[4]
        hourLag = nowHour - publishHour
        minsLag = nowMin - i.updated_parsed[4]
        
        if hourLag == 0 and minsLag <= 30 and minsLag >= 0:
            listHourLag.append(hourLag)
            listMinsLag.append(minsLag)
            listAVNum.append(i.link)
        if hourLag  == 1 and minsLag >= -59 and minsLag <= -31:
            listHourLag.append(hourLag)
            listMinsLag.append(minsLag)
            listAVNum.append(i.link)
        # 解决八小时时差问题
        if nowHour >= 0 and nowHour <= 7 and publishHour >= 24 and publishHour <= 32:
            listHourLag.append(hourLag)
            listMinsLag.append(minsLag)
            listAVNum.append(i.link)
        listAVSet = list(set(listAVNum))
        # print("时间差：" + str(hourLag))
        # print("分钟差: " + str(minsLag))
        print("\n")
        # listHourLag.append(hourLag)
        # listMinsLag.append(minsLag)
        # listAVNum.append(i.link)
    # print(time.localtime())
    # str = "现在的时间是：%d年%d月%d日%d时%d分%d秒" %(time.localtime()[0], time.localtime()[1], time.localtime()[2], time.localtime()[3], 
    #                                                 time.localtime()[4], time.localtime()[5])
    # print(str)
    # print(type(time.localtime()[3]))
    # print('现在时间是：')
    # print(nowHour)
    return listHourLag, listMinsLag, listAVSet

def splitAVLink(avList):
    lastAVLink=[]
    for i in avList:
        avStr = i.split('v', 2)
        lastav = avStr[-1]
        lastAVLink.append(lastav)
    return lastAVLink
        
        
def postBilibili(avid):
    with open('D:/python_practice/bilibiliWatchlater/info.json', 'r') as myfile:
        data = myfile.read()

    obj = json.loads(data)
    # print("username: " + str(obj['username']))
    # print("password:" + str(obj['password']))
    sessdata = str(obj['sessData'])
    csrf = str(obj['CSRF'])
    csrf_token = str(obj['CSRF_TOKEN'])
    for i in avid:
        url = 'https://api.bilibili.com/x/v2/history/toview/add'
        sessdata = sessdata
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }
        res = requests.post(url=url,data={
            'aid': i,
            'jsonp': 'jsonp',
            'csrf': csrf,
            'csrf_token': csrf_token
        }, headers=headers, cookies={"SESSDATA":sessdata}).json()
        print(res)


if __name__ == '__main__':
    print("-----Auto Post Bilibili to Watchlater Starting-----")
    hours, mins, avLink = getRSS()
    av = splitAVLink(avLink)
    postBilibili(av)
    print("添加视频的小时差：")
    print(hours)
    print("添加视频的分钟差：")
    print(mins)
    print("添加的视频av号：")
    print(avLink)
    print("裁剪后的视频av号：")
    print(av)
    print("-----Auto Post Bilibili to Watchlater Finished-----")