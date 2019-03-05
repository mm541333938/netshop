import math

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

# Create your views here.
from goods.models import Category, Goods


class IndexView(View):
    def get(self, request, cid=1, num=1):
        cid = int(cid)
        num = int(num)
        # 查询类别信息
        categorysList = Category.objects.all().order_by('id')
        # 查询当前类别下的所有商品信息
        goodsList = Goods.objects.filter(category_id=cid).order_by('id')

        # 分页(每页8条)
        pager = Paginator(goodsList, 8)
        # 获取当前页
        page_goodsList = pager.page(num)

        # 每页开始页码
        begin = (num - int(math.ceil(10.0 / 2)))
        if begin < 1:
            begin = 1

        # 每页结束页码
        end = begin + 9
        if end > pager.num_pages:
            end = pager.num_pages

        if end <= 10:
            begin = 1
        else:
            begin = end - 9

        pagelist = range(begin, end + 1)

        return render(request, 'netshop/index.html', {
            'categorysList': categorysList,
            'goodsList': page_goodsList,
            'currentCid': cid,
            'pagelist': pagelist,
            'currentNum': num
        })


class DetailView(View):
    def get(self, request, goodsId):
        goodsId = int(goodsId)

        # 根据goodsid 查询商品详情信息(goods对象）
        goods = Goods.objects.get(id=goodsId)

        return render(request, 'netshop/detail.html', {'goods': goods})
