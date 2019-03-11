from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from utils import code

# Create your views here.
from django.views import View

from userapp.models import UserInfo, Area, Address


class RegisterView(View):
    def get(self, request):
        return render(request, 'netshop/register.html')

    def post(self, request):
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')
        # 插入数据库
        user = UserInfo.objects.create(uname=uname, pwd=pwd)

        if user:
            # 将用户信息存放到session对象中
            request.session['user'] = user

            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/register')


class CheckUnameView(View):
    def get(self, request):
        # 获取请求参数
        uname = request.GET.get('uname', '')

        # 查询
        userList = UserInfo.objects.filter(uname=uname)
        flag = False
        if userList:
            flag = True
        return JsonResponse({'flag': flag})


class CenterView(View):
    def get(self, request):
        return render(request, 'netshop/center.html')


class LogoutView(View):
    def post(self, request):
        # 清楚session 中登录用户信息
        if 'user' in request.session:
            del request.session['user']

        return JsonResponse({'delFlag': True})


class LoginView(View):
    def get(self, request):
        return render(request, 'netshop/login.html')

    def post(self, request):
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')

        # 查询数据库中是否存在
        userList = UserInfo.objects.filter(uname=uname, pwd=pwd)
        if userList:
            request.session['user'] = userList[0]
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')


class LoadCodeView(View):
    def get(self, request):
        img, str = code.gene_code()
        # 将生成的验证码发到session中
        request.session['sessionCode'] = str
        return HttpResponse(img, content_type='image/png')


class CheckCodeView(View):
    def get(self, request):
        # 获取input中的值
        code = request.GET.get('code', '')
        # 获取生成的验证码
        sessionCode = request.session.get('sessionCode', None)
        flag = code == sessionCode

        return JsonResponse({'checkFlag': flag})


class AddressView(View):
    def get(self, request):
        # 获取当前用户的收货地址
        addrList = Address.objects.all()

        return render(request, 'netshop/address.html', context={'addrList': addrList})
        return render(request, 'netshop/address.html')

    def post(self, request):
        # 获取请求参数
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user', '')
        # 插入数据库
        address = Address.objects.create(aname=aname, aphone=aphone, addr=addr, userinfo=user,
                                         isdefault=(lambda count: True if count == 0 else False)(
                                             user.address_set.all().count()))

        # 获取当前用户的收货地址
        addrList = Address.objects.all()

        return render(request, 'netshop/address.html', context={'addrList': addrList})


class LoadArea(View):
    def get(self, request):
        # 获取请求参数
        pid = request.GET.get('pid', -1)
        pid = int(pid)

        # 根据父id查询区划信息
        areaList = Area.objects.filter(parentid=pid)

        # 进行序列化
        jareaList = serialize('json', areaList)

        return JsonResponse({'jareaList': jareaList})
