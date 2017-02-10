"""LiveWithPassion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

from django.contrib import admin

admin.autodiscover()

class SimpleStaticView(TemplateView):
    def get_template_names(self):
        return ["ang/app/" + self.kwargs.get('template_name') + ".html"]

    # def get(self, request, *args, **kwargs):
    #     from django.contrib.auth import authenticate, login
    #     if request.user.is_anonymous():
    #         # Auto-login the User for Demonstration Purposes
    #         user = authenticate()
    #         login(request, user)
    #     return super(SimpleStaticView, self).get(request, *args, **kwargs)

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    #url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    # url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^fbaccounts/', include('allauth.urls')),
    url(r'^api/posts/', include('posts.api.urls', namespace='posts-api')),
    url(r'^api/comments/', include('comments.api.urls', namespace='comments-api')),
    url(r'^(?P<template_name>[\w-]+)$', SimpleStaticView.as_view(), name='example'),
    url(r'^$', TemplateView.as_view(template_name='ang/home.html')),
    # url(r'^', include('posts.urls', namespace='posts')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # from django.views.static import serve
    # urlpatterns += [
    #     url(r'^(?P<path>favicon\..*)$', serve, {'document_root': settings.STATIC_ROOT}),
    #     url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], serve, {'document_root': settings.MEDIA_ROOT}),
    #     url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:], serve, dict(insecure=True)),
    # ]