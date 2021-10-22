import requests
import codecs
import re
from time import sleep
from bs4 import BeautifulSoup
def GetCityURl():
    url="http://www.bendibao.com/city.htm"
    headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
            }
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
        if(len(str1)<=4):
            str1=str1+' '*(4-len(str1))
        f.write(str1+'\t'+str+'\n')
    f.close()
    return


def GetURL2():
    f = codecs.open('cityherf.txt', 'r')
    URLs = f.readlines()
    f.close()
    f=codecs.open('cityherf2.txt', 'a')
    headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
            }

    for http in URLs:
        url=http.split()[1]
        url=url.strip('\n')
        print(url)
        city_name=http.split()[0];
        html = requests.get(url=url, headers=headers)
        html.encoding = 'utf-8'
        html_news = html.text
        bs = BeautifulSoup(html_news, 'html.parser')
        try:
            pare=bs.find('form')
            if('search'in pare['action']):
                print(city_name)
                print(pare['action']+'?q=人才落户&p=&s='+pare.input['value'])
        except TypeError as e:
            print("没有找到"+city_name)
        except Exception as e2:
            print('other error')
    f.close()