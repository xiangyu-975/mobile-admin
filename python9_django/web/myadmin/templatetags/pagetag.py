from django import template
register = template.Library()


from django.utils.html import format_html
@register.simple_tag
def cheng(n1,n2):
    n1 = int(n1)
    n2 = float(n2)
    return n1*n2

# 自定分页标签
from django.utils.html import format_html
@register.simple_tag
def fenye(count,request):
    # 获取当前页码数,如果没有默认为第一页
    p = int(request.GET.get('p',1))
    count = int(count)
    # 设置显示多少页码
    begin = p - 4
    end = p + 5

    if p > count-5:
        begin = count - 9
        end = count

    if p < 5:
        begin = 1
        end = 10

    if count < 10:
        begin = 1
        end = count

    # 把地址栏中携带的参数p去掉
    args = ''
    for k,v in request.GET.items():
        if k != 'p':
            args += '&'+k+'='+v

    s = ''

    # 首页
    s += '<li><a href="?p=1'+args+'">首页</a></li>'
    # 判断上一页
    if p == 1:
        s += '<li><a href="?p=1'+args+'">上一页</a></li>'
    else:
        s += '<li><a href="?p='+str(p-1)+args+'">上一页</a></li>'

     # 循环页码数
    for x in range(begin,end+1):
        if x == p:
            s += '<li class="am-active"><a href="?p='+str(x)+args+'">'+str(x)+'</a></li>'
        else:
            s += '<li ><a href="?p='+str(x)+args+'">'+str(x)+'</a></li>'

    # 判断下一页
    if p == count:
        s += '<li><a href="?p='+str(count)+args+'">下一页</a></li>'
    else:
        s += '<li><a href="?p='+str(p+1)+args+'">下一页</a></li>'
    # 尾页
    s += '<li><a href="?p='+str(count)+args+'">尾页</a></li>'


    # 总页数
    s += '<li>共{v}页</li>'.format(v=count)

    return format_html(s)