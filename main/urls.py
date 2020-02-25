from django.conf.urls import url
from main import views
from Personalweb import views as pviews

urlpatterns = [
    url(r'^home-(?P<article_type_id>\d+)', views.home),
    url(r'^home', views.home),
    url(r'^Beeblog',views.Beeblog),
    url(r'^pesonalweb',pviews.personal)
]