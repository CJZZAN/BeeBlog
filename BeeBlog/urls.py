"""BeeBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.main, name='main')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='main')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from main import views
from Personalweb import views as pviews
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^admin/',include(admin.site.urls)),
    url(r'^Beeblog.html', views.Beeblog),
    url(r'^Beeblog$', views.Beeblog),
    url(r'^Beeblog-(?P<article_type_id>\d+)$', views.Beeblog),
    url(r'^Beeblog?keywords=(\S)',views.Beeblog),
    url(r'^Beeblog/(?P<user_id>\d+)-(?P<topic_id>\d+)-(?P<article_id>\d+)',pviews.personal),
    url(r'^Beeblog/(?P<user_id>\d+)-(?P<topic_id>\d+)$',pviews.personal),
    url(r'^Beeblog/(?P<user_id>\d+)-(?P<topic_id>\d+).html',pviews.personal),
    url(r'^Beeblog/blogeditor$',pviews.blogeditor),
    url(r'^Beeblog/blogeditor.html',pviews.blogeditor),
    # url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+)',include("main.urls")),
    url(r'^main/', include("main.urls")),
    url(r'^login/', include("login.urls")),
    url(r'^Beeblog/personalweb', pviews.personal),
    url(r'^ueditor/',include('DjangoUeditor.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
