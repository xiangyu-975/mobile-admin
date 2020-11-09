from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. models import Goods,Types
from . views import uploads

# 添加模板
def add(request):
    ob =  Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
    # ob = Types.objects.all()

    context = {'tlist':ob}

    return render(request,'admin/goods/add.html',context)
    # return HttpResponse('执行添加')

# 执行添加
def insert(request):
    # 导入图片上传函数
    
    if not request.FILES.get('pic',None):
        return HttpResponse('<script>alert("请选择上传的商品图片");location.href="/admin/goods/add/"</script>')
    try:
        ob = Goods()
        ob.typeid = Types.objects.get(id=request.POST['typeid'])
        ob.title = request.POST['title']
        ob.price = request.POST['price']
        ob.storage = request.POST['storage']
        ob.info = request.POST['info']
        ob.pic = uploads(request)
        ob.save()

        return HttpResponse('<script>alert("添加成功");location.href="/admin/goods/list/"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="/admin/hoods/add/"</script>')

def list(request):
    # 搜索类型
    types = request.GET.get('type',None)

    # 搜索条件
    keywords = request.GET.get('keywords','')

    # print(types)
    # print(keywords)

    if types:

        if types == 'title':
            from django.db.models import Q
            ob = Goods.objects.filter(title__contains=keywords)
            print(ob)
    else:
        # 获取所有数据
        ob = Goods.objects.exclude(status=3)
    # 数据分页类
    from django.core.paginator import Paginator
    # 实例化分页类  参数1 查询的数据,参数2 每页要显示的数据
    paginator = Paginator(ob,8)

    # 当前页码
    p = int(request.GET.get('p',1))

    # 根据当前页码获取当前页应该显示的数据
    userlist = paginator.page(p)

    # 获取当前页的页码数 (1,177)
    num = paginator.page_range

    # 分配数据
    context = {'glist':userlist,'pagenum':num}
    # context = {'glist':ob}

    return render(request,'admin/goods/list.html',context)

def goodsstatusupdate(request):
    ob = Goods.objects.get(id=request.GET['uid'])
    ob.status = int(request.GET['status'])
    ob.save()

    return HttpResponse('')



def edit(request,tid):
    
    # 获取所有数据
    ob = Goods.objects.get(id = tid)
    # 分配数据
    context = {'uinfo':ob}

    
    return render(request,'admin/goods/edit.html',context)


def update(request):
    try:
        # 根据id获取用户对象
        ob = Goods.objects.get(id=request.POST['id'])
        ob.title = request.POST.get('title')
        ob.price = request.POST.get('price')
        ob.storage = request.POST.get('storage')
        ob.info = request.POST.get('info')
        print(ob.pic)

        # 判断是否有图片上传
        if request.FILES.get('pic'):
            # 判断是不是使用的默认图片
            if ob.pic != '/static/pics/default/default.jpg':
                import os
                #如过使用的不是默认头像,则删除图片
                os.remove('.'+ob.pic) 
            # 上传新的图片
            ob.pic = uploads(request)

        # 执行更新
        ob.save()
        return HttpResponse('<script>alert("修改成功");location.href="/admin/goods/list/"</script>')
    except:
        return HttpResponse('<script>alert("修改失败");location.href="/admin/goods/list/"</script>')


def delete(request,uid):
    # 逻辑删除数据  并不是从数据苦中删除
    try:
        # 获取数据
        ob = Goods.objects.get(id=uid)
        # 修改状态
        ob.status = 3
        # 执行逻辑删除
        ob.save()

        return HttpResponse('<script>alert("删除成功");location.href="/admin/goods/list/"</script>')
    except:
        return HttpResponse('<script>alert("删除失败");location.href="/admin/goods/list/"</script>')
