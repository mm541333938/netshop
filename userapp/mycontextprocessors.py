#coding=utf-8
# 全局上下文
def getUserInfo(request):
    return {'suser': request.session.get('user', None)}
