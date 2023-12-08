"""
-*- coding:utf-8-sig -*-
@Author: yogurt
"""
import json
import re

from lxml import etree

import Utils

filename = 'www_merrell_com'
headers = {
    'authority': 'www.merrell.com',
    'accept': '*/*',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.merrell.com/US/en/thermo-snowdrift-2-mid-waterproof/58346M.html',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

# kid-footwear-sale/
# 获取详情数据
def getfoodinfo(url, Collection):
    infodata = Utils.request(url,headers=headers)
    infotree = etree.HTML(infodata.text)
    Title = Utils.getxpathdata(infotree.xpath('//div[@class="product-v2-name"]/h1//text()'))
    try:
        Body =  Utils.xpathgetHtml(infotree.xpath('//div[@class="pdp-drawers"]/div')[0],infodata)
    except Exception as e:
        with open('error.txt', 'a', encoding='utf-8-sig') as f:
            f.write(url+'\n')
    id = url.split('/')[-1].split('.html')[0]
    params = {
        'productID': f'{id}',
    }
    response = Utils.request(
        'https://www.merrell.com/on/demandware.store/Sites-merrell_us-Site/default/ProductInfo-GetDimensionsAndVariations',
        params=params,
        headers=headers,
    )
    jsdata = json.loads(response.text)
    colorlist = [item['displayValue'] +',' + item['ID'] for item in jsdata['color']['values']]
    print(colorlist)
    option_1Name = "Color"
    option2_title = 'Size'
    option2_value_title = [sizeitem['value'] for sizeitem in jsdata['size']['values']]
    priceurl = 'https://www.merrell.com/on/demandware.store/Sites-merrell_us-Site/default/ProductInfo-GetProductPrice'
    for colordata in colorlist:
        coloritem = colordata.split(',')[-1]
        option_1Value = [colordata.split(',')[0] + ',htt']
        prarmprcie = {'masterPid':id, 'pid':str(coloritem)}
        pricetext = Utils.request(priceurl, params=prarmprcie)
        VariantPrice = Utils.re_return_str(re.findall('Sale Price[\s\S]*?\$(.*?)\n',pricetext.text))
        VariantCompareAtPrice = Utils.re_return_str(re.findall('Original price[\s\S]*?\$(.*?)\n',pricetext.text))
        imgurl ="https://www.merrell.com/on/demandware.store/Sites-merrell_us-Site/default/ProductInfo-GetProductImages"
        imgprama = {'pid':id , f'dwvar_{id}_color':coloritem}
        res_img = Utils.request(imgurl, params= imgprama)
        imgtree = etree.HTML(res_img.text)
        optionbaseimg = [item.split('?')[0] for item in imgtree.xpath('//div[@id="js-product-image-slider"]//img/@data-src')]
        option_1imgList =[item.split('?')[0] for item in  [optionbaseimg[0]] + imgtree.xpath('//div[@id="js-product-image-slider"]//img/@data-lazy')]
        # print(option_1imgList)
        Utils.baseInfo(filename, url, Body, Collection, Title, option_1Name, option_1Value, option2_title,
                 option2_value_title, optionbaseimg, option_1imgList, VariantCompareAtPrice, VariantPrice,
                 )

    # 分类进行获取颜色
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


        baseInfo(filename, url, Body, Collection, hanlder, Title, option_1Name, option_1Value, option2_title, option2_value_title,optionbaseimg,option_1imgList,VariantCompareAtPrice,VariantPrice,option3_title, option3_value_title)
        '''


# 获取所有url数据
def getallurl(url,Collection):
    page = 1
    while True:
        params = {
            'start': f'{page*48-48}',
            'sz': f'{48}',
        }

        response = Utils.request(url, params=params,
                                headers=headers)
        tree = etree.HTML(response.text)
        getallurllist  = tree.xpath('//*[@id="search-result-items"]//a[@class="thumb-link"]/@href')
        savelistdata = [[item.split('?')[0],Collection] for item in  getallurllist]
        Utils.saveAllJson_fromUrl(filename,savelistdata)
        print("商品数目", len(savelistdata),url, params['start'])
        if len(savelistdata) < 48:
            break
        page += 1

# 定义初始化
def init():
    # https://www.merrell.com/US/en/mens-moab-3-jeep/

    # https://www.merrell.com/US/en/merrell-work-footwear-shop-all/
    listdata = [
#         (
#             [ 'Men,Men-Featured,Men-Featured-New arrivals',
#              'Men,Men-Featured,Men-Featured-Best sellers', 'Men,Men-Featured,Men-Featured-Jeep x moab 3',
#              'Men,Men-Featured,Men-Featured-Top styles $100 & under',
#              'Men,Men-Featured,Men-Featured-Only found at merrell.com', 'Men,Men-Featured,Men-Featured-Merrell 1trl™',
#              'Men,Men-Featured,Men-Featured-Moab hiking collection', 'Men,Men-Featured,Men-Featured-Sale'],
#             ['https://www.merrell.com/US/en/mens-new-arrivals/',
#              'https://www.merrell.com/US/en/mens-best-sellers/',
#              'https://www.merrell.com/US/en/mens-moab-3-jeep/',
#              'https://www.merrell.com/US/en/mens-under-100/',
#              'https://www.merrell.com/US/en/mens-online-only/',
#              'https://www.merrell.com/US/en/1trl/',
#              'https://www.merrell.com/US/en/mens-moab/',
#              'https://www.merrell.com/US/en/mens-discount-boots-shoes/']
#         ),
#         (
#             ['Men,Men-Shop By Activity,Men-Shop By Activity-Hiking', 'Men,Men-Shop By Activity,Men-Shop By Activity-Trail Running', 'Men,Men-Shop By Activity,Men-Shop By Activity-Everyday', 'Men,Men-Shop By Activity,Men-Shop By Activity-Winter', 'Men,Men-Shop By Activity,Men-Shop By Activity-Training', 'Men,Men-Shop By Activity,Men-Shop By Activity-Backpacking', 'Men,Men-Shop By Activity,Men-Shop By Activity-Water-Friendly', 'Men,Men-Shop By Activity,Men-Shop By Activity-Work']
# ,
#             ['https://www.merrell.com/US/en/mens-hiking-boots-shoes/',
#              'https://www.merrell.com/US/en/men-footwear-trail-running/',
#              'https://www.merrell.com/US/en/mens-casual-shoes/',
#              'https://www.merrell.com/US/en/mens-winter-gear/',
#              'https://www.merrell.com/US/en/men-footwear-fitness/',
#              'https://www.merrell.com/US/en/men-activity-backpacking/',
#              'https://www.merrell.com/US/en/men-water-shoes/',
#              'https://www.merrell.com/US/en/merrell-work-footwear-shop-all/']
#         ),
#         (
#             ["Men,Men-Shop By Style,Men-Shop By Style-Shop All Men's Shoes",
#              'Men,Men-Shop By Style,Men-Shop By Style-Slip-Ons', 'Men,Men-Shop By Style,Men-Shop By Style-Sneakers',
#              'Men,Men-Shop By Style,Men-Shop By Style-Boots', 'Men,Men-Shop By Style,Men-Shop By Style-Winter Boots',
#              'Men,Men-Shop By Style,Men-Shop By Style-Barefoot', 'Men,Men-Shop By Style,Men-Shop By Style-Sandals',
#              'Men,Men-Shop By Style,Men-Shop By Style-Wide Widths', 'Men,Men-Shop By Style,Men-Shop By Style-Shoe Care']
# ,
#             ['https://www.merrell.com/US/en/mens-shoes/',
#              'https://www.merrell.com/US/en/mens-slip-on-shoes/',
#              'https://www.merrell.com/US/en/men-footwear-sneakers/',
#              'https://www.merrell.com/US/en/mens-boots/',
#              'https://www.merrell.com/US/en/mens-winter-boots/',
#              'https://www.merrell.com/US/en/men-barefoot/',
#              'https://www.merrell.com/US/en/mens-sandals/',
#              'https://www.merrell.com/US/en/mens-wide-width-boot-shoes/',
#              'https://www.merrell.com/US/en/men-bags--accessories-shoe-care/',
#              ]
#         ),
#         (
#             [
#              'Women,Women-Featured,Women-Featured-New arrivals', 'Women,Women-Featured,Women-Featured-Best sellers',
#              'Women,Women-Featured,Women-Featured-Jeep x moab 3',
#              'Women,Women-Featured,Women-Featured-Top styles $100 & under',
#              'Women,Women-Featured,Women-Featured-Only found at merrell.com',
#              'Women,Women-Featured,Women-Featured-Merrell 1trl™',
#              'Women,Women-Featured,Women-Featured-Moab hiking collection', 'Women,Women-Featured,Women-Featured-Sale']
# ,
#             ['https://www.merrell.com/US/en/womens-new-arrivals/',
#              'https://www.merrell.com/US/en/womens-best-sellers/',
#              'https://www.merrell.com/US/en/womens-jeep-moab-3/',
#              'https://www.merrell.com/US/en/womens-under-100/',
#              'https://www.merrell.com/US/en/womens-online-only/',
#              'https://www.merrell.com/US/en/1trl/',
#              'https://www.merrell.com/US/en/womens-moab/',
#              'https://www.merrell.com/US/en/womens-discount-boots-shoes/']
#         ),
#         (
#             ['Women,Women-Shop By Activity,Women-Shop By Activity-Hiking',
#              'Women,Women-Shop By Activity,Women-Shop By Activity-Trail Running',
#              'Women,Women-Shop By Activity,Women-Shop By Activity-Everyday',
#              'Women,Women-Shop By Activity,Women-Shop By Activity-Winter',
#              'Women,Women-Shop By Activity,Women-Shop By Activity-Training',
#              'Women,Women-Shop By Activity,Women-Shop By Activity-Backpacking',
#              'Women,Women-Shop By Activity,Women-Shop By Activity-Water-Friendly',
#              'Women,Women-Shop By Activity,Women-Shop By Activity-Work']
# ,
#             ['https://www.merrell.com/US/en/womens-hiking-boots-shoes/',
#              'https://www.merrell.com/US/en/women-footwear-trail-running/',
#              'https://www.merrell.com/US/en/womens-casual-shoes/',
#              'https://www.merrell.com/US/en/womens-winter-gear/',
#              'https://www.merrell.com/US/en/women-footwear-fitness/',
#              'https://www.merrell.com/US/en/women-activity-backpacking/',
#              'https://www.merrell.com/US/en/women-water-shoes/',
#              'https://www.merrell.com/US/en/merrell-work-footwear-shop-all/']
#         ),
#         (
#             ["Women,Women-Shop By Style,Women-Shop By Style-Shop All Women's Shoes",
#              'Women,Women-Shop By Style,Women-Shop By Style-Slip-Ons',
#              'Women,Women-Shop By Style,Women-Shop By Style-Sneakers',
#              'Women,Women-Shop By Style,Women-Shop By Style-Boots',
#              'Women,Women-Shop By Style,Women-Shop By Style-Winter Boots',
#              'Women,Women-Shop By Style,Women-Shop By Style-Barefoot',
#              'Women,Women-Shop By Style,Women-Shop By Style-Sandals',
#              'Women,Women-Shop By Style,Women-Shop By Style-Wide Widths',
#              'Women,Women-Shop By Style,Women-Shop By Style-Shoe Care',
#              ]
# ,
#             ['https://www.merrell.com/US/en/womens-shoes/',
#              'https://www.merrell.com/US/en/womens-slip-on-shoes/',
#              'https://www.merrell.com/US/en/women-footwear-sneakers/',
#              'https://www.merrell.com/US/en/womens-boots/',
#              'https://www.merrell.com/US/en/womens-winter-boots/',
#              'https://www.merrell.com/US/en/women-barefoot/',
#              'https://www.merrell.com/US/en/womens-sandals/',
#              'https://www.merrell.com/US/en/womens-wide-width-boot-shoes/',
#              'https://www.merrell.com/US/en/women-bags--accessories-shoe-care/'
#              ]
#         ),
#         (
#             ["Kids,Kids-Shop By Style,Kids-Shop By Style-Shop All Kids' Footwear",
#              'Kids,Kids-Shop By Style,Kids-Shop By Style-Sneakers',
#              'Kids,Kids-Shop By Style,Kids-Shop By Style-Easy On,Easy Off',
#              'Kids,Kids-Shop By Style,Kids-Shop By Style-Boots',
#              'Kids,Kids-Shop By Style,Kids-Shop By Style-Sandals',
#              'Kids,Kids-Shop By Style,Kids-Shop By Style-Wide Widths',
#              'Kids,Kids-Shop By Style,Kids-Shop By Style-Mini Me',
#              'Kids,Kids-Shop By Style,Kids-Shop By Style-Socks & Accessories']
# ,
#             ['https://www.merrell.com/US/en/kids-footwear/',
#              'https://www.merrell.com/US/en/kids-footwear-sneakers/',
#              'https://www.merrell.com/US/en/kids-footwear-slip-ons/',
#              'https://www.merrell.com/US/en/kids-footwear-boots/',
#              'https://www.merrell.com/US/en/kid-footwear-sandals/',
#              'https://www.merrell.com/US/en/kid-featured-wide-widths/',
#              'https://www.merrell.com/US/en/kids-featured-mini-me/',
#              'https://www.merrell.com/US/en/kids-socks-accessories/']
#         ),
#         (
#             ['Kids,Kids-Shop By Activity,Kids-Shop By Activity-Everyday',
#              'Kids,Kids-Shop By Activity,Kids-Shop By Activity-Winter Boots',
#              'Kids,Kids-Shop By Activity,Kids-Shop By Activity-Trail Running',
#              'Kids,Kids-Shop By Activity,Kids-Shop By Activity-Playground',
#              'Kids,Kids-Shop By Activity,Kids-Shop By Activity-Water Shoes',
#              "Kids,Kids-Shop By Activity,Kids-Shop By Activity-Kids' Sale"]
# ,
#             ['https://www.merrell.com/US/en/kids-activity-everyday/',
#              'https://www.merrell.com/US/en/kids-footwear-winter-boots/',
#              'https://www.merrell.com/US/en/kid-footwear-trail-run/',
#              'https://www.merrell.com/US/en/kid-activity-playground/',
#              'https://www.merrell.com/US/en/kids-featured-water-shoes/',
#              'https://www.merrell.com/US/en/kid-footwear-sale/']
#         ),
#         (
#             ['Kids,Kids-Shop By Age,Kids-Shop By Age-Shop All Ages',
#              'Kids,Kids-Shop By Age,Kids-Shop By Age-Little Kid (4 - 10)',
#              'Kids,Kids-Shop By Age,Kids-Shop By Age-Big Kid (10.5 - 7)',
#              'Kids,Kids-Shop By Age,Kids-Shop By Age-Sizing Help']
# ,
#             ['https://www.merrell.com/US/en/shop-kids-all-ages/',
#              'https://www.merrell.com/US/en/kids-footwear-little-kid/',
#              'https://www.merrell.com/US/en/kids-footwear-big-kid/',
#              'https://www.merrell.com/US/en/kids-size-guide/']
#         ),
#         (
#             ["Clothing,Clothing-Men,Clothing-Men-Shop All Men's Clothing", 'Clothing,Clothing-Men,Clothing-Men-Tops',
#              'Clothing,Clothing-Men,Clothing-Men-Bottoms', 'Clothing,Clothing-Men,Clothing-Men-Outerwear',
#              'Clothing,Clothing-Men,Clothing-Men-Sale']
# ,
#             ['https://www.merrell.com/US/en/mens-clothing/',
#              'https://www.merrell.com/US/en/mens-clothing-tops/',
#              'https://www.merrell.com/US/en/mens-pants-shorts/',
#              'https://www.merrell.com/US/en/mens-jackets/',
#              'https://www.merrell.com/US/en/mens-discount-clothing/']
#         ),
#         (
#             ["Clothing,Clothing-Women,Clothing-Women-Shop All Women's Clothing",
#              'Clothing,Clothing-Women,Clothing-Women-Tops', 'Clothing,Clothing-Women,Clothing-Women-Bottoms',
#              'Clothing,Clothing-Women,Clothing-Women-Outerwear', 'Clothing,Clothing-Women,Clothing-Women-Sale'],
#             ['https://www.merrell.com/US/en/womens-clothing/',
#              'https://www.merrell.com/US/en/women-clothing-tops/',
#              'https://www.merrell.com/US/en/womens-pants-shorts/',
#              'https://www.merrell.com/US/en/womens-jackets/',
#              'https://www.merrell.com/US/en/womens-discount-clothing/']
#
#         ),
#         (
#             ['Clothing,Clothing-Accessories,Clothing-Accessories-Shop All Accessories',
#              'Clothing,Clothing-Accessories,Clothing-Accessories-Bags',
#              'Clothing,Clothing-Accessories,Clothing-Accessories-Hats',
#              'Clothing,Clothing-Accessories,Clothing-Accessories-Socks',
#              'Clothing,Clothing-Accessories,Clothing-Accessories-Shoe Care']
# ,
#             ['https://www.merrell.com/US/en/accessories-view-all/',
#              'https://www.merrell.com/US/en/accessories-bags/',
#              'https://www.merrell.com/US/en/accessories-hats-gloves-scarves/',
#              'https://www.merrell.com/US/en/accessories-socks/',
#              'https://www.merrell.com/US/en/accessories-shoe-care/']
#         ),
#         (
#             ['Sale,Sale-Featured,Sale-Featured-Shop All Sale', "Sale,Sale-Featured,Sale-Featured-Kids' Sale",
#              'Sale,Sale-Featured,Sale-Featured-Very Merry Days Of Merrell - Limited Time Deals!',
#              'Sale,Sale-Featured,Sale-Featured-Holiday Leftovers - Up to 50% off!']
# ,
#             ['https://www.merrell.com/US/en/outlet/',
#              'https://www.merrell.com/US/en/kid-footwear-sale/',
#              'https://www.merrell.com/US/en/very-merry-merrell-days/',
#              'https://www.merrell.com/US/en/holiday-sale/']
#         ),
#         (
#             ["Sale,Sale-Women,Sale-Women-Shop All Women's Sale",
#              'Sale,Sale-Women,Sale-Women-Footwear',
#              'Sale,Sale-Women,Sale-Women-Clothing',
#              'Sale,Sale-Women,Sale-Women-Final Sale Up to 60% Off']
# ,
#             [
#              'https://www.merrell.com/US/en/outlet-women/',
#              'https://www.merrell.com/US/en/womens-discount-boots-shoes/',
#              'https://www.merrell.com/US/en/womens-discount-clothing/',
#              'https://www.merrell.com/US/en/womens-last-chance/']
#         ),
#         (
#             ["Sale,Sale-Men,Sale-Men-Shop All Men's Sale",
#              'Sale,Sale-Men,Sale-Men-Footwear',
#              'Sale,Sale-Men,Sale-Men-Clothing',
#              'Sale,Sale-Men,Sale-Men-Final Sale Up to 60% Off']
# ,
#             ['https://www.merrell.com/US/en/outlet-men/',
#              'https://www.merrell.com/US/en/mens-discount-boots-shoes/',
#              'https://www.merrell.com/US/en/mens-discount-clothing/',
#              'https://www.merrell.com/US/en/mens-last-chance/']
#         ),
    ]
    count = 0
    for tulerun in listdata:
        if len(tulerun[0]) != len(tulerun[1]):
            print("名称长度和链接数目不一致，错误所在行数", listdata.index(tulerun),tulerun[0])
        else:
            for indexurl in range(len(tulerun[0])):
                count += 1
                name = tulerun[0][indexurl]
                url = tulerun[1][indexurl]
                getallurl(url, name)
                print("url 存储完成", url, name)


if __name__ == '__main__':
    # init()
    # thredlist = ['Men', "Shop All Men's Sale", 'Footwear', 'Clothing', 'Final Sale Up to 60% Off']
    # Utils.getTagetitle('Sale', '', thredlist)
    # getallurl('1','2')
    # getfoodinfo()
    # Utils.resovelNew('www_merrell_com.json')
    jsdata = Utils.loadjson('www_merrell_com_finly.json')
    count = 0
    for item in jsdata:
        count+=1
        getfoodinfo(item['url'], item['Collection'])
        print("剩余", len(jsdata)-count)
        if count ==2:
            exit()

