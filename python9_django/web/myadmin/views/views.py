from django.shortcuts import render
from django.http import HttpResponse
from .. models import Users,Order
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def index(request):
    return render(request,'admin/index.html')


# 登录页面
def login(request):
    return render(request,'admin/login.html')

# 执行登录页面
def dologin(request):
    # 判断验证码是否正确
    if request.POST['vcode'].upper() != request.session['verifycode'].upper():
        return HttpResponse('<script>alert("验证码错误");location.href="/admin/login/"</script>')
    # 判断用户 密码 权限
    ob = Users.objects.filter(username = request.POST['username'])
    if ob:
        ob = ob[0]
        # 判断密码是否正确
        if check_password(request.POST['password'],ob.password):
            # 判断是否有权限
            if ob.status == 2:
                # 有权限
                request.session['AdminUser'] = {'name':ob.username,'pic':ob.picurl}
                return HttpResponse('<script>alert("登陆成功");location.href="/admin/"</script>')
                

    #         else:
    #             return HttpResponse('<script>alert("没有权限");location.href="/admin/login/"</script>')
                

    #     else:
    #         return HttpResponse('<script>alert("密码错误");location.href="/admin/login/"</script>')

    # else:           
    #     return HttpResponse('<script>alert("用户不存在");location.href="/admin/login/"</script>')
    return HttpResponse('<script>alert("用户或者密码不存在");location.href="/admin/login/"</script>')

# 退出登录
def outlogin(request):
    del request.session['AdminUser']

    return HttpResponse('<script>alert("已退出登录");location.href="/admin/login/"</script>')

# 会员添加
def add(request):

    return render(request,'admin/user/add.html')

# 执行文件上传
def insert(request):
    # 判断图片上传类型
    pic = uploads(request)
    if not pic:
        return HttpResponse('<script>alert("头像图片类型类型不正确,请更改图片类型");location.href="/admin/user/add/"</script>')
    try:
        # 接收数据  进行添加
        ob = Users()
        ob.username = request.POST.get('username')
        # 设置密码加密
        ob.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
        ob.email = request.POST.get('email')
        ob.phone = request.POST.get('phone')
        ob.age = request.POST.get('age')
        ob.sex = request.POST.get('sex')
        ob.picurl = pic
        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="/admin/user/list/"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="/admin/user/add/"</script>')

# 会员列表
def list(request):
    # 搜索类型
    types = request.GET.get('type',None)
    # 搜索条件
    keywords = request.GET.get('keywords',None)

    # 判断是否有搜索条件
    if types:
        # 有搜索条件
        if types == 'all':
            from django.db.models import Q
            data = Users.objects.filter(Q(username__contains=keywords)|Q(email__contains=keywords)|Q(phone__contains=keywords)|Q(age__contains=keywords)|Q(sex__contains=keywords)|Q(status__contains=keywords))
        if types == 'username':
            data = Users.objects.filter(username__contains=keywords)
        if types == 'email':
            data = Users.objects.filter(email__contains=keywords)
        if types == 'phone':
            data = Users.objects.filter(phone__contains=keywords)
        if types == 'age':
            data = Users.objects.filter(age__contains=keywords)
        if types == 'sex':
            data = Users.objects.filter(sex__contains=keywords)
        if types == 'status':
            data = Users.objects.filter(status__contains=keywords)
        
    else:
        # 获取所有用户数据
        data = Users.objects.exclude(status=3)

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(data,5)

    # 获取当前页码
    p = int(request.GET.get('p',1))

    # 获取分页数据对象
    goodslist= paginator.page(p)


    # print(ob)
    # 分配数据
    context = {'ulist':goodslist}
    # 传入数据
    return render(request,'admin/user/list.html',context)

# 状态修改
def userstatusupdate(request):
    ob = Users.objects.get(id=request.GET['uid'])
    ob.status = int(request.GET['status'])
    ob.save()

    return HttpResponse('')

# 会员删除  逻辑删除
def delete(request,uid):
    # 逻辑删除数据  并不是从数据苦中删除
    try:
        # 获取数据
        ob = Users.objects.get(id=uid)
        # 修改状态
        ob.status = 3
        # 执行逻辑删除
        ob.save()

        return HttpResponse('<script>alert("删除成功");location.href="/admin/user/list/"</script>')
    except:
        return HttpResponse('<script>alert("删除失败");location.href="/admin/user/list/"</script>')

# 会员修改
def edit(request,uid):
    # 获取所有数据
    ob = Users.objects.get(id = uid)
    # 分配数据
    context = {'uinfo':ob}

    
    return render(request,'admin/user/edit.html',context)

# 执行修改
def update(request):
    try:
        # 根据id获取用户对象
        ob = Users.objects.get(id=request.POST['id'])
        ob.username = request.POST.get('username')
        ob.email = request.POST.get('email')
        ob.phone = request.POST.get('phone')
        ob.age = request.POST.get('age')
        ob.sex = request.POST.get('sex')

        # 判断是否有图片上传
        if request.FILES.get('pic'):
            # 判断是不是使用的默认图片
            if ob.picurl != '/static/pics/default/default.jpg':
                import os
                #如过使用的不是默认头像,则删除图片
                os.remove('.'+ob.picurl) 
            # 上传新的图片
            ob.picurl = uploads(request)

        # 执行更新
        ob.save()
        return HttpResponse('<script>alert("修改成功");location.href="/admin/user/list/"</script>')
    except:
        return HttpResponse('<script>alert("修改失败");location.href="/admin/user/list/"</script>')

# 图片函数
def uploads(request):
    
    import time,random

    myfile = request.FILES.get('pic',None)
    # 判断是否有文件上传
    if not myfile:
        return '/static/pics/default/default.jpg'

    # 执行文件上传
    # 自定义文件名 时间戳+随机数+.jpg
    filename = str(time.time())+str(random.randrange(10000,99999))

    # 获取当前上传文件的后缀名
    hzm = myfile.name.split('.').pop()
    # 允许上传的文件类型
    arr = ['png','jpg','gif','jpeg','bmp','icon']

    if hzm not in arr:
        return False

    # 打开文件
    file = open('./static/pics/'+filename+'.'+hzm,'wb+')
    # 分块写入文件  
    for chunk in myfile.chunks():      
           file.write(chunk)  
    # 关闭文件
    file.close()

    # 返回文件的url路径
    return '/static/pics/'+filename+'.'+hzm

# 验证码
def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABqwerCD123tyuiEFopGHasdfJK4ghjk56LMNOlPQRzxcvS789TUbnmVWXYZ0'
    # str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

# 订单列表
def dingdanlist(request):
    
    orders = Order.objects.filter(uid=request.session['VipUser']['uid'])

    # 数据分页
    from django.core.paginator import Paginator
    # 实例化分页类
    paginator = Paginator(orders,5)

    # 获取当前页码
    p = int(request.GET.get('p',1))

    # 获取分页数据对象
    goodslist= paginator.page(p)

    context = {'orders':goodslist}

    return render(request,'admin/user/dingdanlist.html',context)

# 订单状态修改
def dingdanstatusupdate(request):
    ob = Order.objects.get(id=request.GET['uid'])
    ob.status = int(request.GET['status'])
    ob.save()

    return HttpResponse('')