from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from cart import cartmanager


class AddCartView(View):
    def post(self, request):
        # 在多级字典数据的时候需要设置这个，能实时存放数据到session中
        request.session.modified = True

        # 获取当前操作类型
        flag = request.POST.get('flag')

        # 判断当前操作类型
        if flag == 'add':
            cartManagerObj = cartmanager.getCartManger(request)
            cartManagerObj.add(**request.POST.dict())

        elif flag == 'plus':

            cartManagerObj = cartmanager.getCartManger(request)
            # 修改数据库数量
            cartManagerObj.update(step=1, **request.POST.dict())

        elif flag == 'minus':
            # 创建对象
            cartManagerObj = cartmanager.getCartManger(request)
            # 修改数据库数量
            cartManagerObj.update(step=-1, **request.POST.dict())

        elif flag == 'delete':
            cartManagerObj = cartmanager.getCartManger(request)
            cartManagerObj.delete(**request.POST.dict())

        return HttpResponseRedirect('/cart/queryAll/')


class QueryAllView(View):
    def get(self, request):
        cartManagerObj = cartmanager.getCartManger(request)

        cartList = cartManagerObj.queryAll()

        return render(request, 'netshop/cart.html', {'cartList': cartList})
