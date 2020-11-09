from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. models import Types

# 添加模板
def add(request):

    # 获取所有数据的所有分类
    # ob = Types.objects.all()
    ob = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')

    context = {'tlist':ob}
    
    return render(request,'admin/types/add.html',context)

# 执行添加
def insert(request):
    try:
    
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        if ob.pid == '0':
            ob.path = '0,'
        else:
            # 如果添加的不是顶级分类
            p = Types.objects.get(id=ob.pid)
            ob.path = p.path + str(ob.pid )+','

        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="/admin/types/list/"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="/admin/types/add/"</script>')

def list(request):
    # 搜索类型
    types = request.GET.get('type',None)

    # 搜索条件
    keywords = request.GET.get('keywords',None)

    # print(types)
    # print(keywords)

    if types:

        if types == 'name':
            from django.db.models import Q
            ob = Types.objects.filter(name__contains=keywords)
    else:
        # 获取所有数据bingqie分类
        ob = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
    for x in ob:
            # 控制当前对象的 缩进
            n =  int(len(x.path) / 2)-1
            x.name = (n*'----')+x.name
            # 给当前对象 添加一个所属父类的属性
            if x.pid == 0:
                x.pname = '顶级分类'
            else:
                obj = Types.objects.get(id=x.pid)
                x.pname = obj.name
    # 数据分页类
    from django.core.paginator import Paginator
    # 实例化分页类  参数1 查询的数据,参数2 每页要显示的数据
    paginator = Paginator(ob,3)

    # 当前页码
    p = int(request.GET.get('p',1))

    # 根据当前页码获取当前页应该显示的数据
    userlist = paginator.page(p)

    # 获取当前页的页码数 (1,177)
    num = paginator.page_range

    # 分配数据
    context = {'tlist':userlist,'pagenum':num}

    # 加载模板
    return render(request,'admin/types/list.html',context)


def delete(request):
    
    num = Types.objects.filter(pid=request.GET['tid']).count()

    if num:

        return JsonResponse({'status':1,'msg':'当前类下还有子类,不能删除'})

    ob = Types.objects.get(id = request.GET['tid'])

    ob.delete()
    return JsonResponse({'status':0,'msg':'可以删除'})

def edit(request,tid):
    ob = Types.objects.get(id=tid)
    fl = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')

    context = {'tinfo':ob,'tlist':fl}
    
    return render(request,'admin/types/edit.html',context)

def update(request):
    try:

        # 获取当前对象,执行修改
        ob = Types.objects.get(id=request.POST['tid'])
        ob.name = request.POST['name']
        ob.save()
    
        return HttpResponse('<script>alert("修改成功");location.href="/admin/types/list/"</script>')
    except:
        return HttpResponse('<script>alert("修改失败");location.href="/admin/types/edit/'+request.POST['tid']+'/"</script>')