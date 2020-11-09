from django import template
register = template.Library()

# 自定义过滤器
# @register.filter
# def kong_upper(val):
#     # print ('val from template:',val)
#     return val.upper()

# 自定义标签
from django.utils.html import format_html
@register.simple_tag
def shows(count,request):
    # count 总页码数 20
    # request  当前页面的请求对象

    # begin  开始页
    # eng  结束页

    # 获取所有参数,在每一次页码跳转时,携带已有的参数
    # <QueryDict: {'type': ['all'], 'keywords': ['41'], 'p': ['2']}>
    # ?keywords=41&type=all
    p = int(request.GET.get('p',1))
    count = int(count)
    
    kv = '' 
    for x in request.GET:
        if x != 'p':
            kv+= '&'+x+'='+request.GET[x]


    begin = p - 1
    end = p + 1


    if p < 2:
        begin = 1
        end = 3
    if p > count - 1:
        begin = count - 2
        end = count

    if count < 4:
        begin = 1
        end = count
    s = ''
    s += '<li><a href="?p=1'+kv+'">首页</a></li>'
    # 上一页 当前页-1
    if p <= 1:
        s += '<li><a href="?p=1'+kv+'">上一页</a></li>'
    else:
        s += '<li><a href="?p='+str(p-1)+kv+'">上一页</a></li>'

    for x in range(begin,end+1):
        # 判断是否为当前页
        if x == p:
            s += '<li class="am-active"><a href="?p='+str(x)+kv+'">'+str(x)+'</a></li>'
        else:
            s += '<li><a href="?p='+str(x)+kv+'">'+str(x)+'</a></li>'

    if p >= count:
        s += '<li><a href="?p='+str(count)+kv+'">下一页</a></li>'
    else:
        s += '<li><a href="?p='+str(p+1)+kv+'">下一页</a></li>'
    s += '<li><a href="?p='+str(count)+kv+'">尾页</a></li>'
    return format_html(s)