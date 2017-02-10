from django.conf.urls import url
from django.contrib import admin

from .views import  (
        post_list,
        post_detail,
        post_delete,
        post_update,
        post_create,
    )

urlpatterns = [
    url(r'^$', post_list, name="list"),
    url(r'(?P<slug>[\w-]+)/$', post_detail, name="detail"),
    url(r'(?P<pk>\d+)/$', post_detail, name="detail"),
    url(r'create$', post_create),
    
    url(r'(?P<slug>[\w-]+)/edit$', post_update, name="update"),
    url(r'(?P<slug>[\w-]+)/delete$', post_delete, name="delete"),
    # url(r'^$', post_list),
]