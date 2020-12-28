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
    listAVSet = []
    listAuthor = []
    listTitle = []
    link2title = {}

    with open('D:/python_practice/bilibiliWatchlater/info.json', "r") as myfile:
        data = myfile.read()

    obj = json.loads(data)
    url = str(obj['URL'])

    rss = feedparser.parse(url)
    
    print(rss.feed.title)
    print("\n")
    
    for i in rss['entries']:
        print("id:"+" "+i['id'])
        print("link:"+" "+i['link'])
        print("title:"+" "+i['title'])
        print("author:"+" "+i['author'])
        print("description:"+" "+i['description'])
        print(i.updated_parsed)
        
        publishHour = i.updated_parsed[3] + 8
        publishMin = i.updated_parsed[4]

        nowDay = time.localtime()[2]
        nowHour = time.localtime()[3]
        nowMin = time.localtime()[4]

        dayLag = nowDay - i.updated_parsed[2]
        hourLag = nowHour - publishHour
        minsLag = nowMin - i.updated_parsed[4]
        
        author = i['author']
        title = i['title']
        link = i['link']
        
        bedtimeFlag = bedtimeNews(author, title)

        if(bedtimeFlag == 1 or bedtimeFlag == 3):
            
            if dayLag == 0:
                
                if hourLag == 0 and minsLag <= 30 and minsLag >= 0:
                    appendItem(listHourLag, listMinsLag, listAVNum, listAuthor, listTitle,
                                hourLag, minsLag, link, author, title)
                    linktotitle(link, title, link2title)
                
                if hourLag  == 1 and minsLag >= -59 and minsLag <= -31:
                    appendItem(listHourLag, listMinsLag, listAVNum, listAuthor, listTitle,
                                hourLag, minsLag, link, author, title)
                    linktotitle(link, title, link2title)
            
            if dayLag == 1:
                
                if nowHour == 0 and publishMin == 23 and publishMin >= 30 and publishMin >= 59:
                    appendItem(listHourLag, listMinsLag, listAVNum, listAuthor, listTitle,
                                hourLag, minsLag, link, author, title)
                    linktotitle(link, title, link2title)
                
                if nowHour >= 0 and nowHour <= 7 and publishHour >= 24 and publishHour <= 32:
                    appendItem(listHourLag, listMinsLag, listAVNum, listAuthor, listTitle,
                                hourLag, minsLag, link, author, title)
                    linktotitle(link, title, link2title)
                
                if nowHour == 8 and nowMin == 0 and publishHour >= 24 and publishHour <= 32:
                    appendItem(listHourLag, listMinsLag, listAVNum, listAuthor, listTitle,
                                hourLag, minsLag, link, author, title)
                    linktotitle(link, title, link2title)
        
        # remove the repeat item
        listAVSet = list(set(listAVNum))
        au2title = key2value(listAuthor, listTitle)

        print("\n")

    return listHourLag, listMinsLag, listAVSet, au2title, link2title

def bedtimeNews(author, title):
    if(author == '观视频工作室'):
        if(title.startswith('【睡前消息')):
            return 1
        else:
            return 2
    else:
        return 3


def splitAVLinkList(avList):
    lastAVLink=[]
    for i in avList:
        avStr = i.split('v', 2)
        lastav = avStr[-1]
        lastAVLink.append(lastav)
    return lastAVLink


def splitAVLinkStr(avStr):
    avStr = avStr.split('v',2)
    avstr = avStr[-1]
    return avstr


def linktotitle(link, title, link2title):
    link = splitAVLinkStr(link)
    link2title[link] = title


def key2value(listA, listB):
    dictResult = dict()
    for i, j in zip(listA, listB):
        if i not in dictResult.keys():
            dictResult[i] = []
        dictResult[i].append(j)
    return dictResult


def appendItem(listA, listB, listC, listD, listE, a, b, c, d, e):
    listA.append(a)
    listB.append(b)
    listC.append(c)
    listD.append(d)
    listE.append(e)


def postBilibili(avid):
    
    with open('D:/python_practice/bilibiliWatchlater/info.json', "r") as myfile:
        data = myfile.read()
    obj = json.loads(data)
    
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
    hours, mins, avLink, author2title, link2title = getRSS()
    av = splitAVLinkList(avLink)
    postBilibili(av)
    print("\n")
    print("添加视频的小时差：")
    print(hours)
    print("添加视频的分钟差：")
    print(mins)
    print("添加的视频av号：")
    print(json.dumps(avLink, indent=4, ensure_ascii=False))
    print("裁剪后的视频av号：")
    print(json.dumps(av, indent=4, ensure_ascii=False))
    print('添加视频的 up主-视频标题:')
    print(json.dumps(author2title, indent=4, ensure_ascii=False))
    print('添加视频的 av号-视频标题:')
    print(json.dumps(link2title, indent=4, ensure_ascii=False))
    print("-----Auto Post Bilibili to Watchlater Finished-----")
