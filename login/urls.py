from django.conf.urls import url
from login import views


urlpatterns = [
    url(r'^register',views.register),
    url(r'^login',views.login),
    url(r'^findpsw',views.findpsw),
    url(r'^setpsw',views.setpsw),
]