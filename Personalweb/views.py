from django.shortcuts import render, redirect, HttpResponse
from login.views import login_check
from main import models
from django.utils.safestring import mark_safe
from django.forms import widgets, fields
from django import forms


# Create your views here.

class BlogAuth(forms.Form):
    title = fields.CharField(max_length=20, error_messages={'required': '标题不能为空',
                                                            'max_length': '标题长度不能超过20'},
                             widget=widgets.TextInput(attrs={'class': 'form-control', 'name': 'title', 'id': 'title',
                                                             'placeholder': '请输入标题'}))
    info = fields.CharField(max_length=300, error_messages={'required': '描述不能为空',
                                                            'max_length': '描述长度不能超过150'},
                            widget=widgets.Textarea(attrs={'class': 'form-control', 'name': 'info', 'id': 'info',
                                                           'placeholder': '此字段将显示于主页链接'}))
    # article_type = fields.ChoiceField(choices=models.ArticleType,error_messages={'required':'文章类型必选'})


# @login_check
def blogeditor(request, *args, **kwargs):
    d = request.session['user_id']
    print(d)
    if request.method == "GET":
        article_type = models.ArticleType.objects.all()
        obj = BlogAuth()
        back = '<a href="http://127.0.0.1:8000/Beeblog/%s-0-0" type="button" class="btn btn-primary">确定</a>' % d
        back = mark_safe(back)
        return render(request, 'blogeditor.html', {'obj': obj, 'back': back,'article_type':article_type})
    if request.method == "POST":
        obj = BlogAuth(request.POST)
        print("1")
        request_form = obj.is_valid()
        if request_form:
            print(1)
            title = request.POST.get('title')
            info = request.POST.get('info')
            content = request.POST.get('content')
            article_type = request.POST.get('article_type')
            print(article_type)
            models.Article.objects.create(article_title=title, article_info=info, article_content=content, usr_id=d,
                                          article_type= models.ArticleType.objects.filter(type_id=article_type)[0])
            return redirect('/Beeblog/%s-0-0' % d)
        return render(request, 'blogeditor.html', {'obj': obj})


a = "0"

u = ""
# @login_check
def personal(request, *args, **kwargs):
    d = request.session['user_id']

    e = models.User.objects.get(user_id=d)
    username = e.user_name

    try:
        global a
        a = kwargs["article_id"]
    except:
        pass
    if request.method == "GET":
        global u
        u = kwargs['user_id']
        user_all = models.User.objects.filter(user_id=u)
        e = kwargs["topic_id"]
        my_str = []
        f = []
        my_collection = ""
        my_manage = ""
        if str(d) == str(u):
            my_collection = '<li><a href="http://127.0.0.1:8000/Beeblog/%s-2-0">收藏</a></li>' % d
            my_manage = '<li><a href="http://127.0.0.1:8000/Beeblog/%s-3-0">管理</a></li>' % d
        my_main = '<li><a href="http://127.0.0.1:8000/Beeblog/%s-0-0">首页</a></li>' % d
        my_editor = '<li><a href="http://127.0.0.1:8000/Beeblog/blogeditor">写博客</a></li>'
        article_c = ""
        article_t = ""
        editor = ""
        label = ""
        user_name = ""
        send_time = ""
        user_header = ""
        cr = ""
        if e == "0":
            my_str = models.Article.objects.filter(usr=u)
            if a != "0":
                my_str = []
                f = models.Article.objects.get(article_id=a)
                author = f.usr.user_name
                user_id = f.usr.user_id
                user_name = '<a style="text-decoration:none" href="http://127.0.0.1:8000/Beeblog/%s-0-0">%s</a>' % (user_id,author)
                user_name = mark_safe(user_name)
                send_time = f.article_sendtime
                user_header = f.usr.user_header
                article_c = f.article_content
                article_t = f.article_title
                comment = models.Comment.objects.filter(article_id=a)
                cr = []
                count = 1
                for c in comment:
                    v1 = c.user_id.user_header
                    v2 = c.user_id.user_name
                    f = c.floor
                    v3 = c.content
                    reply = c.reply_set.all()
                    number = len(reply)
                    val = c.comment_id
                    val1 = "0"
                    print(val)
                    v = '<a>%s</a><a>%s</a><span> #%d楼</span><button style="display:inline-block;float:right" ' \
                        'type="button" class="btn btn-primary" data-toggle="modal" data-target="#myModal" onclick="reply(%s,%s);" >回复</button><div><span>%s</span></div><div id="div%s" ' \
                        'onclick="showAndHidden1(%d,%d)" style="display:block;cursor:pointer;color:#0066cc">查看回复(%d)</div>' \
                        '<div id="div%s" onclick="showAndHidden1(%d,%d)" style="display:none;cursor:pointer">收起' % \
                        (v1, v2, f, val, val1, v3, count, count, count + 1, number, count + 1, count + 1, count)
                    cr.append('<div style="width: 1125px; border-bottom: 2px dashed white;padding: 20px 0">')
                    cr.append(v)

                    for r in reply:
                        z1 = r.user_id.user_header
                        z2 = r.user_id.user_name
                        z5 = r.content
                        val1 = r.reply_id
                        if r.reply_to == "0":
                            z = '<div style="padding-left: 20px"><a>%s</a><a>%s</a><button style="display:inline-block;float:right" type="button" class="btn btn-primary" data-toggle="modal" data-target="#myModal" onclick="reply(%s,%s);" >回复</button><div><span>%s</span></div></div>' % (
                            z1, z2,val,val1, z5)
                            cr.append(z)
                        else:
                            g = reply.filter(reply_id=r.reply_to)
                            for x in g:
                                z3 = x.user_id.user_header
                                z4 = x.user_id.user_name
                                z = '<div style="padding-left: 20px"><a>%s</a><a>%s</a>回复<a>%s</a><a>%s</a><button style="display:inline-block;float:right" type="button" class="btn btn-primary" data-toggle="modal" data-target="#myModal" onclick="reply(%s,%s);" >回复</button><div><span>' \
                                    '%s</span></div></div>' % (z1, z2, z3, z4,val,val1, z5)
                                cr.append(z)
                    cr.append("</div>")
                    cr.append("</div>")
                    count += 2
                cr = "".join(cr)
                cr = mark_safe(cr)
        if e == "1":
            editor = '<div><textarea id="editor"></textarea></div>'

        if e == "2":
            obj = models.Collection.objects.filter(user_id=d)
            for i in obj:
                f.append(i.article_id)
            my_str = models.Article.objects.filter(article_id__in=f)

        if e == "3":
            label = models.Label.objects.filter(user_id=d)
            my_str = models.Article.objects.filter(article_user=d)

            # my_str = models.Article.objects.get(article_id__in=obj)

        my_main = mark_safe(my_main)
        my_collection = mark_safe(my_collection)
        my_editor = mark_safe(my_editor)
        my_manage = mark_safe(my_manage)
        editor = mark_safe(editor)

        return render(request, 'personalweb.html', {'article_t': article_t, 'article_c': article_c, 'my_main': my_main,
                                                    'my_str': my_str, 'my_collection': my_collection, 'a': a, 'd': d,
                                                    'my_editor': my_editor, 'editor': editor, 'my_manage': my_manage,
                                                    'label': label, 'user_name': user_name, 'send_time': send_time,
                                                    'user_header': user_header, 'cr': cr,'username':username,'user_all':user_all})
    if request.method == "POST":
        # s = request.POST.get("checked",None)
        # label_id = request.POST.get("label_id",None)
        # article_id = request.POST.get("article_id",None)
        # print(label_id)
        # print(article_id)
        # if s == 'true':
        #     models.ArticleLabel.objects.create(label_id=label_id,article_id=article_id)
        # else:
        #     models.ArticleLabel.objects.filter(label_id=label_id,article_id=article_id).delete()
        # return HttpResponse("OK")\
        if not request.POST.get('reply_to', None):
            content = request.POST.get('comment', None)
            if not content:
                return redirect('/Beeblog/%s-0-%s' % (d, a))
            reply = request.POST.get('reply', None)
            user_id = d
            floor = len(models.Comment.objects.filter(article_id=a)) + 1
            print(content, a, user_id, floor)
            orderlist = {
                "content": content,
                "article_id": a,
                "user_id": models.User.objects.filter(user_id=d)[0],
                "floor": floor
            }
            models.Comment.objects.create(**orderlist)
            return redirect('/Beeblog/%s-0-%s' % (u, a))
        else:
            message_text = request.POST.get('message_text', None)
            if not message_text:
                return HttpResponse("Failed")
            comment_id = request.POST.get('comment_id', None)
            print(comment_id)
            reply_to = request.POST.get('reply_to',None)
            replylist = {
                "reply_to": reply_to,
                "content": message_text,
                "comment_id": models.Comment.objects.filter(comment_id=comment_id)[0],
                "user_id": models.User.objects.filter(user_id=d)[0]
            }
            models.Reply.objects.create(**replylist)
            return HttpResponse("OK")
