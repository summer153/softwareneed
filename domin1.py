import requests
import codecs
import re
from time import sleep
import os
from bs4 import BeautifulSoup
def GetCityURl():
    url="http://www.bendibao.com/city.htm"
    headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
            }
    city_name_list = ["北京", "上海", "广州",
                      "成都", "杭州", "重庆", "西安", "苏州",
                      "武汉", "南京", "天津", "郑州", "长沙",
                      "东莞", "佛山", "青岛", "沈阳"]
    html=requests.get(url=url,headers=headers)
    html.encoding='utf-8'
    html_news=html.text
    bs=BeautifulSoup(html_news,'html.parser')
    paras = bs.find('div',class_='city-list')
    f=codecs.open("cityherf.txt",'w')
    paras=paras.find_all('a')
    for i in paras:
        str=i['href']
        str1=i.text
        if(str1 in city_name_list):
            f.write(str1+'\t'+str+'\n')
            print('已经获取'+str1+'的url')
    f.close()
    return


def GetURL2():
    f = codecs.open('cityherf.txt', 'r')
    URLs = f.readlines()
    f.close()
    f=codecs.open('cityherf2.txt', 'w')
    headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
            }

    for http in URLs:
        url=http.split()[1]
        url=url.strip('\n')
        city_name=http.split()[0];
        html = requests.get(url=url, headers=headers)
        html.encoding = 'utf-8'
        html_news = html.text
        bs = BeautifulSoup(html_news, 'html.parser')
        try:
            pare=bs.find('form')
            print(city_name+'拼接搜索url已完成')
            f.write(city_name+'\t'+pare['action']+'?q=人才落户&p=&s='+pare.input['value']+'\n')
        except Exception as e:
            print('other error')
    f.close()
def GetInformation():
    f=codecs.open('cityherf2.txt ','r')
    URLs=f.readlines()
    f.close()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    for url in URLs:
        city_name=url.split()[0]
        url = url.split()[1]
        url=url.split('p=')
        url1=url[0]+'p={}'+url[1]
        txt_name = 'city\\' + '{}的人才落户政策.txt'.format(city_name);
        page=3  #爬取的页数
        f=codecs.open(txt_name,'w')
        for i in range(page):
            url=url1.format(i)
            print(url)
            html=requests.get(url,headers=headers)
            html.encoding = 'utf-8'
            html_news = html.text
            bs = BeautifulSoup(html_news, 'html.parser')

            datas=bs.find_all('h3',class_='c-title')
            for data in datas:
                url =data.find('a')['href']
                text=data.find('a').text
                f.write(text+' '+url+'\n')
        f.close()
def GetMoreInformation(city_name):
    if (os.path.exists(city_name)==False):
        p=os.getcwd()
        os.mkdir(p+'\\'+city_name)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    txt_name ='city\\' + '{}的人才落户政策.txt'.format(city_name);
    f=codecs.open(txt_name,'r')
    Items=f.readlines()
    f.close()
    for item in Items:
        if ("人才"in item and"补贴" in item) or ("落户"in item and"条件" in item) :
            name=item.split()[0]
            name=name.strip('-')
            url=item.split()[2]
            html=requests.get(url,headers=headers)
            html.encoding = 'utf-8'
            html_news = html.text
            bs = BeautifulSoup(html_news, 'html.parser')
            f=codecs.open(city_name+'\\'+name+'.txt','w')
            pares=bs.find('div',class_='title daoyu')
            pares1=bs.find('div',class_='content')
            title=pares.find('h1')
            time=pares.find('span',class_='time')
            form=pares.find('span',class_='form')
            print(title.text)
            print(time.text)
            print(form)
            print(form.text)
            pa=pares.find('p')
            print(pa.text)
            pa1=pares1.find_all('p')
            for item in pa1:
                print(item.text)

            f.close()