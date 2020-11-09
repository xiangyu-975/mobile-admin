"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . views import views,typeviews,goodsviews

urlpatterns = [
    # 后台首页
    url(r'^$', views.index,name='adminindex'),
    # 登录页面
    url(r'^login/$', views.login,name='adminlogin'),
    # 退出登录
    url(r'^outlogin/$', views.outlogin,name='adminoutlogin'),
    # 执行登录页面
    url(r'^dologin/$', views.dologin,name='admindologin'),
    # 验证码
    url(r'^getcode/$', views.verifycode,name='getcode'),

    # 会员管理
    url(r'^user/add/$',views.add,name='amdin_add'),
    url(r'^user/insert/$',views.insert,name='amdin_insert'),
    url(r'^user/list/$',views.list,name='amdin_list'),
    url(r'^user/statusupdate/$',views.userstatusupdate,name='admin_statusupdate'),
    url(r'^user/del/(?P<uid>[0-9]+)$',views.delete,name='amdin_del'),
    url(r'^user/edit/(?P<uid>[0-9]+)$',views.edit,name='amdin_edit'),
    url(r'^user/update/$',views.update,name='amdin_update'),
    # 订单列表
    url(r'^dingdan/list/$',views.dingdanlist,name='dingdan_list'),
    # 订单状态修改
    url(r'^dingdanstatusupdate/$',views.dingdanstatusupdate,name='dingdan_statusupdate'),


    # 商品分类管理
    url(r'^types/add/$',typeviews.add,name='type_add'),
    url(r'^types/insert/$',typeviews.insert,name='type_insert'),
    url(r'^types/list/$',typeviews.list,name='type_list'),
    url(r'^types/del/$',typeviews.delete,name='type_del'),
    url(r'^types/edit/(?P<tid>[0-9]+)$',typeviews.edit,name='type_edit'),
    url(r'^types/update/$',typeviews.update,name='type_update'),

    # 商品管理
    url(r'^goods/add/$',goodsviews.add,name='good_add'),
    url(r'^goods/insert/$',goodsviews.insert,name='good_insert'),
    url(r'^goods/list/$',goodsviews.list,name='good_list'),
    url(r'^goods/statusupdate/$',goodsviews.goodsstatusupdate,name='good_statusupdate'),
    url(r'^goods/edit/(?P<tid>[0-9]+)$',goodsviews.edit,name='good_edit'),
    url(r'^goods/update/$',goodsviews.update,name='good_update'),
    url(r'^goods/del/(?P<uid>[0-9]+)$',goodsviews.delete,name='good_del'),





]
