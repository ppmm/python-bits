# usr/bin/python3
# coding: utf-8
# author: syw

import tushare as ts
import pandas as pd
from pandas import Series, DataFrame
from datetime import date

class QuotationCrawler():

    def __init__(self):
        pass

    def crawl_hist_data(self):
        pass

class FundamentalCrawler():

    def __init__(self):

        self.funclist = [('业绩报告（主表）',ts.get_report_data),
                         ('盈利能力',ts.get_profit_data),
                         ('营运能力',ts.get_operation_data),
                         ('成长能力',ts.get_growth_data),
                         ('偿债能力',ts.get_debtpaying_data),
                         ('现金流量',ts.get_cashflow_data)]
        pass

    def crawl(self):
        today = date.today()
        year = today.year
        month = today.month
        today = today.strftime('%Y%m%d')
        writer = pd.ExcelWriter('data/基本面数据_'+today+'.xlsx')
        data = ts.get_stock_basics()
        data.to_excel(writer,'股票列表')
        for name,func in self.funclist:
            for m in [1,2,3,4]:
                sheet = name+'_2015年第'+str(m)+'季度'
                print(sheet+'：正在抓取......')
                data = func(2015,m)
                print(sheet+'：抓取完成！')
                data.to_excel(writer,sheet)
            for m in range(1,month//3+1):
                sheet = name+'_2016年第'+str(m)+'季度'
                print(sheet+'：正在抓取......')
                data = func(2016,m)
                print(sheet+'：抓取完成！')
                data.to_excel(writer,sheet)
        writer.save()

class MacroCrawler():

    def __init__(self):
        self.funclist = [('存款利率',ts.get_deposit_rate),
                     ('贷款利率',ts.get_loan_rate),
                     ('存款准备金率',ts.get_rrr),
                     ('货币供应量',ts.get_money_supply),
                     ('货币供应量(年底余额)',ts.get_money_supply_bal),
                     ('国内生产总值(年度)',ts.get_gdp_year),
                     ('国内生产总值(季度)',ts.get_gdp_quarter),
                     ('三大需求对GDP贡献',ts.get_gdp_for),
                     ('三大产业对GDP拉动',ts.get_gdp_pull),
                     ('三大产业贡献率',ts.get_gdp_contrib),
                     ('居民消费价格指数',ts.get_cpi),
                     ('工业品出厂价格指数',ts.get_ppi)]

    def crawl(self):
        today = date.today().strftime('%Y%m%d')
        writer = pd.ExcelWriter('data/宏观经济数据_'+today+'.xlsx')
        for name,func in self.funclist:
            print(name+'：正在抓取......')
            data = func()
            data.to_excel(writer,name)
            print(name+'：抓取完成！')
        writer.save()

class ClassificationCrawler():

    def __init__(self):
        self.funclist = [('行业分类',ts.get_industry_classified),
                         ('概念分类',ts.get_concept_classified),
                         ('地域分类',ts.get_area_classified),
                         ('中小板分类',ts.get_sme_classified),
                         ('创业板分类',ts.get_gem_classified),
                         ('风险警示板分类',ts.get_st_classified),
                         ('沪深300成份及权重',ts.get_hs300s),
                         ('上证50成份股',ts.get_sz50s),
                         ('中证500成份股',ts.get_zz500s),
                         ('终止上市股票列表',ts.get_terminated),
                         ('暂停上市股票列表',ts.get_suspended)]

    def crawl(self):
        today = date.today().strftime('%Y%m%d')
        writer = pd.ExcelWriter('data/股票分类数据_'+today+'.xlsx')
        for name,func in self.funclist:
            print(name+'：正在抓取......')
            data = func()
            data.to_excel(writer,name)
            print(name+'：抓取完成！')
        writer.save()

def main():
    fc = FundamentalCrawler()
    fc.crawl()



if __name__ == '__main__':
    main()


