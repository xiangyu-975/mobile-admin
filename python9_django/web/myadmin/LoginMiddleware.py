from django.shortcuts import render
from django.http import HttpResponse
import re

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        urllist = ['/admin/login/','/admin/dologin/','/admin/getcode/']
        # 判断是否进入后台
        if re.match('/admin/',request.path) and request.path not in urllist:
            if not request.session.get('AdminUser',None):
                return HttpResponse('<script>alert("请先登录");location.href="/admin/login/"</script>')

        # 判断是否有要进入前台需要登录的页面
        urllist = ['/order/confirm/','/order/caerte/','/order/buy/','/myorder/','/myuser/']
        # 判断是否进入
        if request.path in urllist:

            # 判断是否登录
            if not request.session.get('VipUser',None):
                # 如果没有登录,则跳转到登录页面
                return HttpResponse('<script>alert("请先登录");location.href="/login/"</script>')

        response = self.get_response(request)
        return response