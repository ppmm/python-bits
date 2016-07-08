#! /usr/bin/python3
# coding:utf-8

'''
获取人力资源和社会保障部的解决夫妻两地分居情况公示的全部数据；
网站主页为：http://www.mohrss.gov.cn/；
'''

from pandas import DataFrame
import requests
from lxml import etree

class MohrssCrawler():

    def __init__(self):
        pass

    def resolve_page(self,url):
        data = {'year':[],
                'id':[],
                'unit':[],
                'inbj':[],
                'transfer':[],
                'child':[]}
        xp1 = '//*[@id="div1"]/div[1]/div[1]/div[1]'
        xp2 = '//*/tbody'
        r = requests.get(url)
        r.encoding = 'utf-8'
        html = etree.HTML(r.text)
        year = int(html.xpath(xp1)[0].text[:4])
        tbody = html.xpath(xp2)[0]
        for tr in tbody[1:]:
            id,unit,inbj,transfer,child = self.resolve_tr(tr)
            data['year'].append(year)
            data['id'].append(id)
            data['unit'].append(unit)
            data['inbj'].append(inbj)
            data['transfer'].append(transfer)
            data['child'].append(child)
        df = DataFrame(data,columns=['year','id','unit','inbj','transfer','child'])
        return df

    def resolve_tr(self,tr):
        id = tr[0][0][0][0].text
        unit = tr[1][0][0][0].text
        inbj = tr[2][0][0][0].text
        transfer = tr[3][0][0][0].text
        try:
            child = tr[4][0][0][0].text
        except IndexError:
            child = None
        return id,unit,inbj,transfer,child

    def resolve_url(self):
        surl = 'http://search.mohrss.gov.cn/was5/web/search?page=%d'\
               +'&channelid=226064&searchword=%E8%A7%A3%E5%86%B3%E5%A4%AB%E5%A6%BB%E4%B8%A4%E5%9C%B0%E5%88%86%E5%B1%85%E6%83%85%E5%86%B5%E5%85%AC%E7%A4%BA&keyword=%E8%A7%A3%E5%86%B3%E5%A4%AB%E5%A6%BB%E4%B8%A4%E5%9C%B0%E5%88%86%E5%B1%85%E6%83%85%E5%86%B5%E5%85%AC%E7%A4%BA&orderby=-DOCRELTIME&perpage=10&outlinepage=10&searchscope=&timescope=&timescopecolumn=&orderby=-DOCRELTIME&andsen=&total=&orsen=&exclude='
        urls = []
        for i in range(1,8):
            r = requests.get(surl % i)

        return urls

def main():
    url = 'http://www.mohrss.gov.cn/SYrlzyhshbzb/zwgk/gggs/tg/201605/t20160510_239721.html'
    mc = MohrssCrawler()
    x = mc.resolve_page(url)
    print(x)

if __name__ == '__main__':
    main()