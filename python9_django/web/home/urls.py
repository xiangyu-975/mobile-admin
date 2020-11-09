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
from . import views

urlpatterns = [
    # 首页
    url(r'^$', views.index,name='index' ),
    # 登录
    url(r'^login/$', views.login,name='login' ),
    # 执行登录
    url(r'^dologin/$', views.dologin,name='dologin' ),
    # 注册
    url(r'^register/$', views.register,name='register' ),
    # 执行注册
    url(r'^doregister/$', views.doregister,name='doregister' ),
    # 退出登录
    url(r'^outlogin/$', views.outlogin,name='outlogin' ),
    

    # 列表页
    url(r'^list/(?P<tid>[0-9]+)$', views.list,name='list' ),
    # 购买页
    url(r'^info/(?P<gid>[0-9]+)$', views.info,name='info' ),
    # 加入购物车
    url(r'^cart/add/$',views.cartadd,name='cartadd'),
    # 购物车列表
    url(r'^cart/list/$',views.cartlist,name='cartlist'),
    # 清空购物车
    url(r'^cart/clear/$',views.cartclear,name='cartclear'),
    # 商品删除
    url(r'^cart/del/(?P<sid>[0-9]+)$',views.delete,name='shanchu'),
    # 商品数量加减
    url(r'^cart/edit/$',views.cartedit,name='cartedit'),


    # 下单
    # 订单确认
    url(r'^order/confirm/$',views.orderconfirm,name='orderconfirm'),
    # 生成订单
    url(r'^order/create/$',views.ordercreate,name='ordercreate'),
    # 付款
    url(r'^order/buy/$',views.orderbuy,name='orderbuy'),
    # 我的订单
    url(r'^myorder/$',views.myorder,name='myorder'),
    # 个人中心 地址管理
    url(r'^myxin/$',views.myxin,name='myxin'),
    # 修改地址
    url(r'^addressedit/(?P<aid>[0-9]+)$',views.addressedit,name='addressedit'),
    # 执行修改
    url(r'^addressupdate/$',views.addressupdate,name='addressupdate'),
    # 地址删除
    url(r'^adsressdel/(?P<bid>[0-9]+)$',views.adsressdel,name='adsressdel'),









]
