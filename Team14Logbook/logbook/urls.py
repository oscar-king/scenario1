from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.logbook_list, name='logbook_list'),
    url(r'^create/$', views.logbook_create, name='logbook_create'),
    url(r'^(?P<slug>[\w-]+)/$', views.logbook_detail, name='logbook_detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.logbook_update, name='logbook_update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.logbook_delete, name='logbook_delete'),
]
