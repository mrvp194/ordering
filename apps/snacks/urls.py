from django.conf.urls import url, include
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index, name='index'),    
    url(r'^new$', views.new, name='new'),
    url(r'^create$', views.create, name='create'),
    url(r'^cart$', views.cart, name='cart'),
    # url(r'^checkout$', views.checkout, name='checkout'),
    url(r'^(?P<id>[0-9]+)/create$', views.review, name='review'),
    url(r'^(?P<id>[0-9]+)/add$', views.add, name='add'),
    url(r'^(?P<id>[0-9]+)$', views.show, name='show'),
    url(r'^(?P<id>[0-9]+)/redit$', views.redit, name='redit'),
    url(r'^(?P<id>[0-9]+)/update$', views.update, name='update'),
    url(r'^reviews/(?P<id>[0-9]+)/update$', views.rupdate, name='rupdate'),
    url(r'^(?P<id>[0-9]+)/destroy$', views.destroy, name='destroy'),
    url(r'^search$', views.search, name='search')
]