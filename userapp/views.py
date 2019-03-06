from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from userapp.models import UserInfo


class RegisterView(View):
    def get(self, request):
        return render(request, 'netshop/register.html')

    def post(self, request):
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')
        # 插入数据库
        user = UserInfo.objects.create(uname=uname, pwd=pwd)

        if user:
            return HttpResponse('True')
        return HttpResponse('False')


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
