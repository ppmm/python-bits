#! /usr/bin/python3
# coding:utf-8

'''
北京住房和城乡建设委员会官方网站数据获取；
网站主页为：http://www.bjjs.gov.cn/；
'''

import requests
import datetime
from lxml import etree
from pandas import DataFrame

class BJRealEstate():

    def __init__(self):
        self.BASE_URL = 'http://www.bjjs.gov.cn/'
        self.FYHYLB_BASE_URL = 'http://210.75.213.188/shh/portal/newbjjs/audit_house_list.aspx'

    def get_onepage_fyhylb(self,pagenumber=1,pagesize=10):
        '''获取一页的房源核验列表数据；'''

        print('房源核验列表：正在处理第'+str(pagenumber)+'页')
        fyhylb = DataFrame(columns=['district','cell','layout','area',\
                                    'price','agency','time','houseid'])
        #区县,小区名称,户型,面积,拟售价格,发布机构,时间,房源编号
        fyhylb.index.name = 'checkid'       #核验编号
        url = self.FYHYLB_BASE_URL+'?pagenumber=%d&pagesize=%d' % (pagenumber,pagesize)
        r = requests.get(url)
        html = etree.HTML(r.text)
        houselist = html.xpath('//*[@class="houseList"]/tbody/tr')
        for house in houselist:
            checkid,info = self._parse_fyhylb(house)
            fyhylb.loc[checkid] = info
        return fyhylb

    def _parse_fyhylb(self,house):
        '''将房源核验列表中的一行解析出来；'''

        info = []
        tds = house.getchildren()
        for td in tds[1:-1]:
            info.append(td.text)
        info[3] = float(info[3])#面积
        info[6] = datetime.datetime.strptime(info[6],'%Y-%m-%d')#时间
        info.append(int(tds[-1].getchildren()[0].values()[0].split('=')[1]))#房源编号
        checkid = int(tds[0].text)#核验编号
        return checkid,info

    def _get_totalpage_fyhylb(self):
        '''获取房源核验列表的总页数；'''

        r = requests.get(self.FYHYLB_BASE_URL)
        html = etree.HTML(r.text)
        pagenum = html.xpath('//td[@nowrap]')[1].text.split('/')[1][:3]
        return int(pagenum)

    def get_all_fyhylb(self):
        '''获取所有的房源核验列表数据；'''

        pagenum = self._get_totalpage_fyhylb()
        df = self.get_onepage_fyhylb(1)
        for i in range(2,pagenum+1):
            try:
                df = df.append(self.get_onepage_fyhylb(i))
            except:
                print('第'+str(i)+'页发生错误！')
        return df

    def get_one_fyhyxx(self,house_id):
        '''根据house_id获取一条房源核验信息；'''
        pass

    def get_all_fyhyxx(self):
        '''获取所有的房源核验信息；'''
        pass

def main():
    today = datetime.date.today().strftime('%Y%m%d')
    filename = '../data/bjjs.gov.cn_房源核验列表_'+today+'.xlsx'
    sheetname = '房源核验列表'
    bjre = BJRealEstate()
    bjre.get_all_fyhylb().to_excel(filename,sheetname)

if __name__ == '__main__':
    main()