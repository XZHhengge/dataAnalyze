from django.shortcuts import render
import time

from taobao.models import *
from taobao.serializers import *

from utils.scrapy_web import ScrapyInfo, scrapy_JD


def index(request):
    return render(request, 'index.html')


# def show(request, id):
#     mydict = {}
#     if(ProductName.objects.filter(jdProductId=id)):
#         taobaoProductId = request.session['taobaoproductId']
#         mydict['jdproductid'] = id
#         mydict['taobaoproductId'] = taobaoProductId
#         print(mydict)
#         return render(request, 'show2.html', mydict)
#
#     else:
#         keyword = request.session['keyword']
#         taobaoProductId = request.session['taobaoproductId']
#         # 初始化类
#         spider = ScrapyInfo(jdid=id, taobaoProductId=taobaoProductId, keyword=keyword)
#         # 开始爬取京东
#         jdlist = spider.scrapy_JDinfo()
#         # taobaolist = spider.scrapy_taobaoinfo()
#         # scrapy_info(id=id)
#
#         #     comments = JDCommentItem.objects.all()[:3]
#         # 饼图
#         # jdpie = pie(jdlist[0], jdlist[1])
#         # # comment_item = json.loads(text1[0], strict=False)['comments'][:3]
#         #
#         # taobaopie = pie2(taobaolist[0], taobaolist[1])
#         # # 云词图
#         # jdworldud = worldcloud(jdlist[2], jdlist[3])
#
#         jdcomments = JDCommentItem.objects.all()[:3]
#         taobaocomments = TaobaoComment.objects.all()[:10]
#         price = JDProductsItem.objects.get(productid=id).reallyPrice
#         # mydict = dict(jdpie, **jdworldud)
#         mydict['jdcomments'] = jdcomments
#         mydict['taobaocomments'] = taobaocomments
#         url = JDProductsItem.objects.get(name=keyword).url
#         mydict['url'] = url
#         mydict['price'] = price
#         mydict['taobaoproductid'] = taobaoProductId
#
#     return render(request, 'show2.html', mydict)


def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('search')
        # request.session['keyword'] = keyword
        # request['keyword'] = keyword
        # 判断是否已经爬过
        if(ProductName.objects.filter(name=keyword)):
            print('已经爬取过京东，跳过')
        else:
            print('没爬过,先获取jd的id并生成')
            id = scrapy_JD(keyword)
            spider = ScrapyInfo(jdid=id, keyword=keyword)
            spider.scrapy_JDinfo()
            print('开始爬取京东')


        # 判断是否爬过淘宝
        if ProductName.objects.get(name=keyword).taobaoProductId == '0':
            # 爬取淘宝
            print('开始爬取淘宝')
            import requests

            url = 'http://127.0.0.1:6800/schedule.json'
            dictdata = {"project": 'default', "spider": 'taobao', 'keyword': '{}'.format(keyword)}

            r = requests.post(url=url, data=dictdata)
            print(r.text)

        else:
            print(ProductName.objects.get(name=keyword).taobaoProductId)
            print('已经爬取过淘宝，跳过')

        # 取到id
        try:
            taobaoid = ProductName.objects.get(name=keyword).taobaoProductId
        except Exception:
            time.sleep(2)
            taobaoid = ProductName.objects.get(name=keyword).taobaoProductId
        jdid = ProductName.objects.get(name=keyword).jdProductId
        jd = JDProductsItem.objects.get(productid=jdid)
        jdurl = jd.url
        jdprice = jd.reallyPrice
        dict = {}

        # taobao
        try:
            taobao = TaobaoProduct.objects.filter(productid=taobaoid)[0]
            taobaoprice = taobao.productprice
            taobaourl = taobao.producturl
            dict['taobaoprice'] = taobaoprice
            dict['taobaourl'] = taobaourl
        except Exception as e:
            print(e)

            # taobao = TaobaoProduct.objects.filter(productid=taobaoid)[0]

        # 取评论
        taobaocomments = TaobaoComment.objects.filter(productid=taobaoid)[:10]
        jdcomments = JDCommentItem.objects.filter(productid=jdid)[:10]
        dict['jdid'] = jdid
        dict['jdurl'] = jdurl
        dict['jdprice'] = jdprice
        dict['taobaoid'] = taobaoid
        dict['taobaocomments'] = taobaocomments
        dict['jdcomments'] = jdcomments
        dict['suningid'] = 1241541
    return render(request, 'show2.html', dict)











