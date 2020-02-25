from django.shortcuts import render,redirect
from main import models
from django.utils.safestring import mark_safe
from login.views import login_check
from django.db.models import Q

# Create your views here.


def Beeblog(request,*args,**kwargs):
    if request.method == "GET":
        request.session['is_login'] = False
        condition = {}
        try:
            c = kwargs['article_type_id'] # 获取当前文章类型的值，为分页做定位，如果不存在则为0
        except:
            c = 0
        try:
            d = request.GET.get('keywords')
        except:
            d = ""
        for k, v in kwargs.items():
            kwargs[k] = int(v)
            if v == '0':
                pass
            else:
                condition[k] = v
        article_type_list = models.ArticleType.objects.all()[:4]
        e = models.ArticleType.objects.all()[4:]
        for i in e:
            print(i.type_name)
        result = models.Article.objects.filter(**condition)
        per_page = 20
        page_num = 4
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        a = []
        for i in result:
            a.append(i)
        data = a[(current_page - 1) * per_page:(current_page) * per_page]
        count_page = len(a)
        total_count, y = divmod(count_page, per_page)
        if y:
            total_count += 1
        page_list = []

        if total_count < page_num:
            start_index = 1
            end_index = total_count + 1
        else:
            if current_page <= (page_num + 1) / 2:
                start_index = 1
                end_index = page_num + 1
            else:
                if current_page + (page_num - 1) / 2 > total_count:
                    start_index = total_count - page_num + 1
                    end_index = total_count + 1
                else:
                    start_index = current_page - (page_num - 1) / 2
                    end_index = current_page + (page_num + 1) / 2

        if current_page == 1:
            prev = '<li><a href="javascript:void(0);" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'
        else:
            prev = '<li><a href="Beeblog-%s.html?p=%s" aria-label="Previous"><span aria-hidden="true">«</span></a></li>' % (c,current_page - 1)
        page_list.append(prev)
        for i in range(int(start_index), int(end_index)):
            if i == current_page:
                temp = '<li><a style=" background-color: #E2E2E2;" href="Beeblog-%s.html?p=%s">%s</a></li>' % (c,i, i)
            else:
                temp = '<li><a href="Beeblog-%s.html?p=%s">%s</a></li>' % (c,i, i)
            page_list.append(temp)
        if current_page == total_count:
            nex = '<li><a href="javascript:void(0);" aria-label="Next"><span aria-hidden="true">»</span></a></li>'
        else:
            nex = '<li><a href="Beeblog-%s.html?p=%s" aria-label="Next"><span aria-hidden="true">»</span></a></li>' % (c,current_page + 1)
        page_list.append(nex)
        # jump = """
        #     <input type='text' /><a onclick='jumpTo(this, "/page/?p=");'>Go</a>
        #     <script>
        #         function jumpTo(ths,base){
        #             var val = ths.previousSibling.value;
        #             location.href = base + val;
        #             }
        #     </script>
        #     """
        # page_list.append(jump)
        search_keywords = request.GET.get('keywords', None)
        if search_keywords:
            result = models.Article.objects.filter(Q(article_title__icontains=search_keywords)
                                                   |Q(article_info__icontains=search_keywords)
                                                   |Q(article_content__icontains=search_keywords))
                                                     # 根据关键词搜索数据库记录，icontains是不区分大小写
            a = []
            for i in result:
                a.append(i)
            data = a[(current_page - 1) * per_page:(current_page) * per_page]
            count_page = len(a)
            total_count, y = divmod(count_page, per_page)
            if y:
                total_count += 1

            if total_count < page_num:
                start_index = 1
                end_index = total_count + 1
            else:
                if current_page <= (page_num + 1) / 2:
                    start_index = 1
                    end_index = page_num + 1
                else:
                    if current_page + (page_num - 1) / 2 > total_count:
                        start_index = total_count - page_num + 1
                        end_index = total_count + 1
                    else:
                        start_index = current_page - (page_num - 1) / 2
                        end_index = current_page + (page_num + 1) / 2
            page_list = []
            if current_page == 1:
                prev = '<li><a href="javascript:void(0);" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'
            else:
                prev = '<li><a href="Beeblog?keywords=%s&p=%s" aria-label="Previous"><span aria-hidden="true">«</span></a></li>' % (
                d, current_page - 1)
            page_list.append(prev)
            for i in range(int(start_index), int(end_index)):
                if i == current_page:
                    temp = '<li><a style=" background-color: #E2E2E2;" href="Beeblog?keywords=%s&p=%s">%s</a></li>' % (
                    d, i, i)
                else:
                    temp = '<li><a href="Beeblog?keywords=%s&p=%s">%s</a></li>' % (d, i, i)
                page_list.append(temp)
            if current_page == total_count:
                nex = '<li><a href="javascript:void(0);" aria-label="Next"><span aria-hidden="true">»</span></a></li>'
            else:
                nex = '<li><a href="Beeblog?keywords=%s&p=%s" aria-label="Next"><span aria-hidden="true">»</span></a></li>' % (
                d, current_page + 1)
            page_list.append(nex)

        pag_str = "".join(page_list)
        pag_str = mark_safe(pag_str)
        print(pag_str)
        top_list = models.Article.objects.all()
        return render(request,'Beeblog.html',{'article_type_list':article_type_list,'arg_dict':kwargs,'result': result,
                                              'a':data,'pag_str':pag_str,'else_list':e,'top_list':top_list})
    # elif request.method == "POST":




@login_check
def home(request,*args,**kwargs):
    username = request.session['username']
    id = request.session['user_id']
    condition = {}
    my_main = '<li><a href="http://127.0.0.1:8000/Beeblog/%s-0.html">我的主页</a></li>' % id
    my_main = mark_safe(my_main)
    try:
        c = kwargs['article_type_id'] # 获取当前文章类型的值，为分页做定位，如果不存在则为0
        print(c)
    except:
        c = 0
    try:
        d = request.GET.get('keywords')
    except:
        d = ''
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v == '0':
            pass
        else:
            condition[k] = v
    article_type_list = []
    obj = models.User.objects.get(user_id=id)
    f = obj.articletype_set.all()
    for z in f:
        article_type_list.append(z.type_id)
    e = models.ArticleType.objects.all().exclude(type_id__in=article_type_list)
    print(e)
    result = models.Article.objects.filter(**condition)
    per_page = 20
    page_num = 4
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    a = []
    for i in result:
        a.append(i)
    data = a[(current_page - 1) * per_page:(current_page) * per_page]
    count_page = len(a)
    total_count, y = divmod(count_page, per_page)
    if y:
        total_count += 1
    page_list = []

    if total_count < page_num:
        start_index = 1
        end_index = total_count + 1
    else:
        if current_page <= (page_num + 1) / 2:
            start_index = 1
            end_index = page_num + 1
        else:
            if current_page + (page_num - 1) / 2 > total_count:
                start_index = total_count - page_num + 1
                end_index = total_count + 1
            else:
                start_index = current_page - (page_num - 1) / 2
                end_index = current_page + (page_num + 1) / 2

    if current_page == 1:
        prev = '<li><a href="javascript:void(0);" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'
    else:
        prev = '<li><a href="/main/home-%s.html?p=%s" aria-label="Previous"><span aria-hidden="true">«</span></a></li>' % (
        c, current_page - 1)
    page_list.append(prev)
    for i in range(int(start_index), int(end_index)):
        if i == current_page:
            temp = '<li><a style=" background-color: #E2E2E2;" href="/main/home-%s.html?p=%s">%s</a></li>' % (c, i, i)
            # temp = '<li><a style=" background-color: #E2E2E2;" href="home.html?p=%s">%s</a></li>' % (i, i)
        else:
            temp = '<li><a href="/main/home-%s.html?p=%s">%s</a></li>' % (c, i, i)
            # temp = '<li><a href="home.html?p=%s">%s</a></li>' % (i, i)
        page_list.append(temp)
    if current_page == total_count:
        nex = '<li><a href="javascript:void(0);" aria-label="Next"><span aria-hidden="true">»</span></a></li>'
    else:
        nex = '<li><a href="/main/home-%s.html?p=%s" aria-label="Next"><span aria-hidden="true">»</span></a></li>' % (
        c, current_page + 1)
    page_list.append(nex)
    # jump = """
    #     <input type='text' /><a onclick='jumpTo(this, "/page/?p=");'>Go</a>
    #     <script>
    #         function jumpTo(ths,base){
    #             var val = ths.previousSibling.value;
    #             location.href = base + val;
    #             }
    #     </script>
    #     """
    # page_list.append(jump)
    search_keywords = request.GET.get('keywords', None)
    if search_keywords:
        result = models.Article.objects.filter(Q(article_title__icontains=search_keywords)
                                               | Q(article_info__icontains=search_keywords)
                                               | Q(article_content__icontains=search_keywords))
        # 根据关键词搜索数据库记录，icontains是不区分大小写
        a = []
        for i in result:
            a.append(i)
        data = a[(current_page - 1) * per_page:(current_page) * per_page]
        count_page = len(a)
        total_count, y = divmod(count_page, per_page)
        if y:
            total_count += 1

        if total_count < page_num:
            start_index = 1
            end_index = total_count + 1
        else:
            if current_page <= (page_num + 1) / 2:
                start_index = 1
                end_index = page_num + 1
            else:
                if current_page + (page_num - 1) / 2 > total_count:
                    start_index = total_count - page_num + 1
                    end_index = total_count + 1
                else:
                    start_index = current_page - (page_num - 1) / 2
                    end_index = current_page + (page_num + 1) / 2
        page_list = []
        if current_page == 1:
            prev = '<li><a href="javascript:void(0);" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'
        else:
            prev = '<li><a href="home?keywords=%s&p=%s" aria-label="Previous"><span aria-hidden="true">«</span></a></li>' % (
                d, current_page - 1)
        page_list.append(prev)
        for i in range(int(start_index), int(end_index)):
            if i == current_page:
                temp = '<li><a style=" background-color: #E2E2E2;" href="home?keywords=%s&p=%s">%s</a></li>' % (
                    d, i, i)
            else:
                temp = '<li><a href="home?keywords=%s&p=%s">%s</a></li>' % (d, i, i)
            page_list.append(temp)
        if current_page == total_count:
            nex = '<li><a href="javascript:void(0);" aria-label="Next"><span aria-hidden="true">»</span></a></li>'
        else:
            nex = '<li><a href="home?keywords=%s&p=%s" aria-label="Next"><span aria-hidden="true">»</span></a></li>' % (
                d, current_page + 1)
        page_list.append(nex)
    pag_str = "".join(page_list)
    pag_str = mark_safe(pag_str)
    top_list = models.Article.objects.all()

    return render(request, 'home.html', {'article_type_list':f,'arg_dict':kwargs,'else_list':e,
                                         'result': result,'a':data,'pag_str':pag_str,'username':username,
                                         'my_main':my_main,'top_list':top_list})

def article(request, *args, **kwargs):
    # print(kwargs)
    # print(kwargs.items)
    # reverse('article',kwargs=kwargs)
    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        print(k,v)
        if v == '0':
            pass
        else:
            condition[k] = v

    article_type_list = models.ArticleType.objects.all()
    result = models.Article.objects.filter(**condition)
    return render(
        request,
        'article.html',
        {
        'result':result,
        'article_type_list':article_type_list,
        'arg_dict':kwargs
        }
    )