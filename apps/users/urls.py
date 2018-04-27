from django.conf.urls import url, include
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index, name='index'),    
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^(?P<id>[0-9]+)$', views.show, name='show'),
    url(r'^(?P<id>[0-9]+)/update$', views.update, name='update'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^admin$', views.admin, name='admin'),
    url(r'^addadmin/(?P<id>[0-9]+)$', views.addadmin, name='addadmin')
]