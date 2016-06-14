#! /usr/bin/python3
# coding:utf-8

'''
历年北京市职工年平均工资数据获取与分析
'''

import requests
from datetime import datetime
from lxml import etree
from pandas import DataFrame

class BJWorksAverageWage():

    def __init__(self):
        self.url = 'http://www.bjrbj.gov.cn/bmfw/ywml/201601/t20160112_55858.html'
        self.wagelist = DataFrame(columns=['wage'])

    def crawl(self):
        r = requests.get(self.url)
        html = etree.HTML(r.text)
        tbody = html.xpath('//*/tbody')[0]
        for i, tr in enumerate(tbody):
            if i == 0:
                pass
            elif i == 1:
                year = datetime.strptime(tr[0][0].text,'%Y')
                wage = float(tr[1][0].text)
                self.wagelist.loc[year] = [wage]
            else:
                year = datetime.strptime(tr[0][0][0].text,'%Y')
                wage = float(tr[1][0][0].text)
                self.wagelist.loc[year] = [wage]
        print(self.wagelist.index)

def main():
    bjwaw = BJWorksAverageWage()
    bjwaw.crawl()

if __name__ == '__main__':
    main()