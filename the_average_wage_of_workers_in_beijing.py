#! /usr/bin/python3
# coding:utf-8

'''
历年北京市职工年平均公司数据获取与分析
'''

import requests
from lxml import etree

class BJWorksAverageWage():

    def __init__(self):
        self.url = 'http://www.bjrbj.gov.cn/bmfw/ywml/201601/t20160112_55858.html'

    def crawl(self):
        r = requests.get(self.url)
        html = etree.HTML(r.text)
        lst = html.xpath('//*/tbody')[0]
        for item in lst[2:]:
            t = item[0][0][0].text
            print(t)

def main():
    bjwaw = BJWorksAverageWage()
    bjwaw.crawl()

if __name__ == '__main__':
    main()