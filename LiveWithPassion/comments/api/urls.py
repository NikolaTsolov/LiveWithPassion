from django.conf.urls import url
from django.contrib import admin

from .views import (
        comment_detail,
        comment_list,
        comment_create,
    )

urlpatterns = [
    #url(r'list', post_list, name="list"),
    url(r'create/$', comment_create, name="create"),
    url(r'(?P<pk>\d+)/$', comment_detail, name="thread"),
    url(r'$', comment_list, name="list"),
    #url(r'(?P<slug>[\w-]+)/edit$', post_update, name="update"),
    #url(r'(?P<slug>[\w-]+)/delete$', comment_delete, name="delete"),
    #url(r'^$', post_list),
]