"""
-*- coding:utf-8-sig -*-
@Author: yogurt
"""
import json
import pprint
import re

from lxml import etree

import Utils

filename = 'spiderinfo'


# 获取详情数据
def getfoodinfo(item):
    url = item['url']
    res = Utils.request(url)
    Collection = item['Collection']
    text = re.findall('productJSON = (.*\}),', res.text)[0]
    jsdata = json.loads(text)
    Body = jsdata['description']
    optionbaseimg = []
    option_1imgList = ['https:'+ item for item in jsdata['images']]
    Title = jsdata['title']
    VariantCompareAtPrice = ''
    if jsdata['compare_at_price']:
        VariantCompareAtPrice = str(jsdata['compare_at_price']//100)
    VariantPrice = str(jsdata['price'] // 100)
    option2_value_title = []
    option_1Value = []
    option3_value_title = []
    for coloroption in jsdata['variants']:
        optioncount = 0
        if coloroption['option1']:
            option_1Name = jsdata['options'][optioncount]
            if coloroption['option1']+ f',{coloroption["option3"]}' not in option_1Value:
                optionbaseimg.append('https:'+jsdata['featured_image'])
                option_1Value.append(coloroption['option1']+ f',{coloroption["option3"]}')
            optioncount+=1
        if coloroption['option2']:
            option2_title = jsdata['options'][optioncount]
            if coloroption['option2'] not in option_1Value:
                option2_value_title.append(coloroption['option2'])
            optioncount += 1
        if coloroption['option3']:
            option3_title = jsdata['options'][optioncount]
            if coloroption['option3'] not in option_1Value:
                option3_value_title.append(coloroption['option3'])

    # print(optionbaseimg,option2_value_title, option_1Value, option_1imgList, VariantPrice)
    # exit()
    Utils.baseInfo(filename, url, Body, Collection, Title, option_1Name, option_1Value, option2_title, option2_value_title,
             optionbaseimg, option_1imgList, VariantCompareAtPrice, VariantPrice, option3_title,
             option3_value_title)

    # Title = Utils.getxpathdata(tree.xpath('//h1[@itemprop="name"]//text()'))
    # Body = Utils.xpathgetHtml(tree.xpath('//section[@class="de-ProductInformation-entry de-u-spaceBottom6"]')[0],res)  # 商品详情信息,需要对 button  超链接进行处理
    # VariantCompareAtPrice = Utils.re_return_str(re.findall('CompareAtPrice: "\$(.*?)"',res.text))  # 原价
    # if VariantCompareAtPrice == '0.00':
    #     VariantCompareAtPrice = ''
    # VariantPrice = Utils.re_return_str(re.findall('Price: "\$(.*?)"',res.text))  # 售价 若没有售价价格为  原价*.3

    # print(Title, VariantPrice, VariantCompareAtPrice)
    '''
    Collection = '3,4,5,5'  # 分类 用,进行分隔
    url = ''  # 产品链接
    Title = ''  # 标题
    Body = '' # 商品详情信息,需要对 button  超链接进行处理
    option_1Name = 'color'
    option_1Value = ['00000,333']  # 用逗号进行分割对应上每一张变量图片
    option2_title = 'size'
    option2_value_title = ['39', '40','41']
    optionbaseimg = ['imgbase',]    #商品主图列表   唯一一张 数量与颜色分类一致
    option_1imgList= ['333img1', ]  #产品变量图片列表  一个商品拥有多张图需注意 只有option_1Value 在图片存在才会找到
    VariantCompareAtPrice = ''    #原价
    VariantPrice = ''   #售价 若没有售价价格为  原价*.3
    '''





# 获取所有url数据
def getallurl():
    pass


# 定义初始化
def init():
    listdata = [
        (
            [],
            []
        ),
        (

        ),
        (

        ),

    ]
    count = 0
    for tulerun in listdata:
        if len(tulerun[0]) != len(tulerun[1]):
            print("名称长度和链接数目不一致，错误所在行数", listdata.index(tulerun))
        else:
            for indexurl in range(len(tulerun[0])):
                count += 1
                name = tulerun[0][indexurl]
                url = tulerun[1][indexurl]


if __name__ == '__main__':
    # thredlist = ['Featured', 'Text a Specialist', 'New arrivals', 'Best sellers', 'Jeep x moab 3',
    #              'Top styles $100 & under', 'Only found at merrell.com', 'Merrell 1trl™', 'Moab hiking collection',
    #              'Sale']
    #
    # Utils.getTagetitle('Men', '', thredlist)
    jsdata = Utils.loadjson("info_decath_finly.json")
    count = 0
    for item in jsdata:
        count+=1
        getfoodinfo(item)
        print("剩余", len(jsdata)-count,list(item.values()))
        # if count == 3:
        #     exit()
