from django.conf.urls import url, include
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index, name='index'),    
    url(r'^new/(?P<id>[0-9]+)?$', views.new, name='new'),
    # url(r'^create$', views.create, name='create'),
    url(r'^create$', views.create, name='create'),
    url(r'^cart$', views.cart, name='cart'),
    url(r'^checkout$', views.checkout, name='checkout'),
    url(r'^newlyadded$', views.newlyadded, name='newlyadded'),
    url(r'^top$', views.top, name='top'),
    url(r'^inventory$', views.inventory, name='inventory'),
    url(r'^mostreviewed$', views.mostreviewed, name='mostreviewed'),
    url(r'^(?P<id>[0-9]+)/create$', views.review, name='review'),
    url(r'^(?P<id>[0-9]+)/quantity$', views.quantity, name='quantity'),
    url(r'^(?P<id>[0-9]+)/add$', views.add, name='add'),
    url(r'^(?P<id>[0-9]+)$', views.show, name='show'),
    url(r'^(?P<id>[0-9]+)/redit$', views.redit, name='redit'),
    url(r'^(?P<id>[0-9]+)/update$', views.update, name='update'),
    url(r'^reviews/(?P<id>[0-9]+)/update$', views.rupdate, name='rupdate'),
    url(r'^(?P<id>[0-9]+)/destroy$', views.destroy, name='destroy'),
    url(r'^(?P<id>[0-9]+)/destroysnack$', views.destroysnack, name='destroysnack'),
    url(r'^search$', views.search, name='search')
]