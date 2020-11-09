from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from myadmin.models import Users,Types,Goods,Address,Order,OrderInfo
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session 

# Create your views here.

def erji():
    # 获取所有顶级分类
    data = Types.objects.filter(pid = 0)
    return data

# 首页
def index(request):

    # 获取顶级分类
    data = Types.objects.filter(pid = 0)
    for x in data:
        x.sub = Types.objects.filter(pid = x.id)
        for y in x.sub:
            y.sub = Goods.objects.filter(typeid=y.id)[:4]


    context = {'typelist':erji(),'ilist':data}

    return render(request,'home/index.html',context)
# 列表页
def list(request,tid):

    # 根据id获取当前分类的信息
    tod = Types.objects.get(id=tid)
    if tod.pid == 0:
        # 顶级分类
        data = tod
        # 获取子类 [{},{}]
        data.sub = Types.objects.filter(pid=tod.id)
        ids = []
        for x in data.sub:
            ids.append(x.id)
        
        data.goods = Goods.objects.filter(typeid__in=ids)

        # {'name':'服装','sub':[{'name':'男装'},{'name':'女装'}],'goods':[{},{},{},{}]}

    else:
        # {'name':'服装','sub':[{'name':'男装'},{'name':'女装'}],'goods':[{},{}],'obj':{'name':'男装'}}
        
        # 先获取父级对象
        data = Types.objects.get(id=tod.pid)
        # 获取当前子类的商品信息
        data.goods = Goods.objects.filter(typeid=tod.id)
        # 获取所有的同级信息,包括当前类
        data.sub = Types.objects.filter(pid=tod.pid)
        # 给data数据追加了一个obj对象
        data.obj = tod



    context = {'typelist':erji(),'data':data}
    return render(request,'home/list.html',context)

# 加入购物车
def cartadd(request):
    try:
        # 接收商品id
        gid = request.GET['gid']
        # 加入购物车的数量
        num = int(request.GET['num'])
        print(num)
        print(gid)

        # 获取购物车数据
        data = request.session.get('cart',{})
        
        # 判断商品是否已经存在与购物车中
        # {1:{},2:{}}
        if gid in data:
            # 如果已经存在,找到商品,修改数量
            data[gid]['num'] += num
        else:
            # 获取商品信息
            goods = Goods.objects.get(id=gid)
            # 把新的商品信息,追加到data数据中
            data[gid] = {'id':goods.id,'title':goods.title,'price':str(goods.price),'pic':goods.pic,'num':num}


        # 加入到session {1:{},2:{}}
        request.session['cart'] = data


        return JsonResponse({'code':0,'msg':'加入购物车成功'})
    except:
        return JsonResponse({'code':1,'msg':'加入购物车失败'})

# 购物车列表
def cartlist(request):


    context = {'typelist':erji()}
    return render(request,'home/cartlist.html',context)

# 清空购物车
def cartclear(request):

    request.session['cart'] = {}

    return HttpResponse('<script>location.href="/cart/list/"</script>')

# 商品数量加减
def cartedit(request):
    gid = request.GET.get('gid')
    num = int(request.GET.get('num'))

    # 读取购物车中的商品

    data = request.session['cart']

    # 修改商品数量
    data[gid]['num'] = num

    # 把数据加载到session中
    request.session['cart'] = data

    return HttpResponse('')

# 确认订单
def orderconfirm(request):

    

    if request.method == 'GET':

        # 获取用户选择的商品
        ids = request.GET['ids'].split(',')
        
        # 从session中读取购物车信息
        cartdata = request.session['cart']
        orderdata = {}

        for x in cartdata:
            if x in ids:
                orderdata[x] = cartdata[x]

        # 把用户选择购买的商品存入session
        request.session['order'] = orderdata

        # 需要让用户确认收货地址 获取当前用户的所有地址信息
        address = Address.objects.filter(uid=request.session['VipUser']['uid'])

        context = {'typelist':erji(),'address':address}
        return render(request,'home/orderconfirm.html',context)

    elif request.method == 'POST':

        # 执行地址的添加
        ob = Address()
        ob.uid = Users.objects.get(id=request.session['VipUser']['uid'])
        ob.aname = request.POST['aname']
        ob.aphone = request.POST['aphone']
        ob.aads = request.POST['aads']

        # 状态修改
        s = request.POST.get('status',0)
        # 判断当前如果设置为默认值,
        if s == '1':
            # 把其它的地址修改状态 0 
            obs = Address.objects.filter(id = request.session['VipUser']['uid']).filter(status=1)
            for x in obs:
                x.status = 0
                x.save()

        ob.status = s
        ob.save()
        return HttpResponse('<script>alert("地址添加成功");location.href="/order/confirm/?ids='+request.GET['ids']+'"</script>')

# 生成订单
def ordercreate(request):
    # 在session中获取商品数据
    data = request.session['order']

    totalprice = 0
    totalnum = 0

    for x in data:
        
        n = float(data[x]['price']) * data[x]['num']

        totalprice += n
        totalnum += data[x]['num']
    # 创建订单
    order = Order()
    order.uid = Users.objects.get(id = request.session['VipUser']['uid'])
    order.address = Address.objects.get(id=request.POST['addressid'])
    order.totalprice = totalprice
    order.totalnum = totalnum
    order.status = 1
    order.save()

    # 先读取购物车里面的数据
    cart = request.session['cart']

    # 创建订单详情
    for x in data:
        orderinfo = OrderInfo()
        orderinfo.orderid = order
        goods = Goods.objects.get(id = x)
        orderinfo.gid = goods
        orderinfo.num = data[x]['num']
        orderinfo.price = data[x]['price']
        orderinfo.save()
        # 将购物车中的商品删除
        del cart[x]

        # 修改狗台数据
        goods.num += data[x]['num']
        goods.storage -= data[x]['num']
        goods.save()

    # 清空session中的订单数据
    request.session['order'] = {}
    # 更新购物车
    request.session['cart'] = cart


    # 跳转到付款页面
    return HttpResponse('<script>alert("订单创建成功,请立即支付");location.href="/order/buy/?orderid='+str(order.id)+'"</script>')

# 付款
def orderbuy(request):
    
    orderid = request.GET.get('orderid',None)
    if orderid:
        # 通过订单id获取订单信息,并展示
        order = Order.objects.get(id=orderid)

        times='<a href="'+reverse('index')+'">手动跳转</a>'
        dataend='秒后将自动跳转'
        context = {'typelist':erji(),'order':order,'d':dataend,'t':times}
        return render(request,'home/fukuan.html',context)

# 详情页
def info(request,gid):
    
    # 根据id获取商品的信息
    ginfo = Goods.objects.get(id=gid)

    context = {'typelist':erji(),'ginfo':ginfo}
    return render(request,'home/buy.html',context) 

# 登录页
def login(request):

    return render(request,'home/login.html')

# 退出登录
def outlogin(request):
    del request.session['VipUser']
    return HttpResponse('<script>alert("已退出登录");location.href="/"</script>')
    
# 执行登录
def dologin(request):
    # 判断验证码是否正确
    if request.POST['code'].lower() != request.session['verifycode'].lower():
        return HttpResponse('<script>alert("验证码错误");location.href="/login/"</script>')
    # 判断用户是否存在
    ob = Users.objects.filter(username = request.POST['username'])
    if ob:
        ob = ob[0]
        # 判断密码是否正确
        if check_password(request.POST['password'],ob.password):
            request.session['VipUser'] = {'name':ob.username,'pic':ob.picurl,'uid':ob.id}

            return HttpResponse('<script>alert("登陆成功");location.href="/"</script>')

    return HttpResponse('<script>alert("用户或者密码不存在");location.href="/login/"</script>')

# 注册页
def register(request):

    return render(request,'home/register.html')

# 执行注册页
def doregister(request):
    aa = request.POST['username']
    bb = request.POST['password']
    if not aa:
        return HttpResponse('<script>alert("请输入用户名");location.href="/register/"</script>')
    if not bb:
        return HttpResponse('<script>alert("请输入密码");location.href="/register/"</script>')

    else:
        # 判断用户名是否存在
        res = Users.objects.filter(username=request.POST['username']).exists()

        if res:
            return HttpResponse('<script>alert("用户名已经存在");location.href="/register/"</script>')
        else:
            ob = Users()
            ob.username = request.POST['username']
            ob.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
            ob.save()

            request.session['VipUser'] = {'name':ob.username,'pic':ob.picurl,'uid':ob.id}

            return HttpResponse('<script>alert("注册成功");location.href="/"</script>')

# 购物车删除
def delete(request,sid):

    aa = request.session['cart']

    del aa[sid]

    request.session['cart'] = aa

    return HttpResponse('<script>location.href="/cart/list/"</script>')
    
# 我的订单
def myorder(request):
    # 查询所有信息
    orders = Order.objects.filter(uid=request.session['VipUser']['uid'])
    # 分配数据
    context = {'typelist':erji(),'orders':orders}
    return render(request,'home/myorder.html',context)

# 地址管理
def myxin(request):
    address = Address.objects.filter(uid=request.session['VipUser']['uid'])
    print(address)
    # 分配数据
    context = {'typelist':erji(),'address':address}

    return render(request,'home/zhongxin.html',context)

# 修改地址
def addressedit(request,aid):
    # 获取地址数据
    ad = Address.objects.get(id = aid)

    # 分配数据
    context = {'tyoelist':erji(),'adlist':ad}
    return render(request,'home/addressedie.html',context)

# 执行修改
def addressupdate(request):
    
    ad = Address.objects.get(id = request.POST['id'])
    ad.aname = request.POST.get('aname')


    ad.aads = request.POST.get('aads')
    ad.aphone = request.POST.get('aphone')
    ad.save()
    return HttpResponse('<script>alert("修改成功");location.href="/myxin/"</script>')

# 地址删除
def adsressdel(request,bid):
    
    ad = Address.objects.get(id = bid)

    ad.delete()

    return HttpResponse('<script>alert("删除成功");location.href="/myxin/"</script>')

