from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from cart import cartmanager


class AddCartView(View):
    def post(self, request):
        # 获取当前操作类型
        flag = request.POST.get('flag')

        # 判断当前操作类型
        if flag == 'add':
            cartManagerObj = cartmanager.getCartManger(request)
            cartManagerObj.add(**request.POST.dict())

        return HttpResponseRedirect('/cart/queryAll/')


class QueryAllView(View):
    def get(self, request):
        cartManagerObj = cartmanager.getCartManger(request)

        cartList = cartManagerObj.queryAll()

        return render(request, 'netshop/cart.html', {'cartList': cartList})
