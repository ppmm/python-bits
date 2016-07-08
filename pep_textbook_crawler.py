#! /usr/bin/python3
# coding:utf-8

'''
从人民教育出版社官方网站爬取电子课本；
'''

import requests
from lxml import etree


class TextBookCrawler():

    def __init__(self):
        self.baseurl = 'http://www.pep.com.cn/gzls/js/tbjx/kb/dzkb/bx1/201008/'

        pass

    def crawl(self):
        for i in range(2,137):
            suffix = 831450-i
            url = self.baseurl + 't20100830_'+str(suffix)+'.htm'
            r = requests.get(url)
            html = etree.HTML(r.text)
            try:
                imgurl = html.xpath('//*[@id="doccontent"]/img')[0].get('src')
            except:
                print('Exception:',i)
                continue
            imgurl = self.baseurl+imgurl[2:]
            self.saveimg(imgurl,i)
            print('Successful:',i)

    def saveimg(self,imgurl,pagenum):
        page = requests.get(imgurl)
        pagename = '../test/'+str(pagenum)+'.jpg'
        with open(pagename, 'wb') as test:
            test.write(page.content)

def main():
    tbc = TextBookCrawler()
    tbc.crawl()

if __name__ == '__main__':
    main()
