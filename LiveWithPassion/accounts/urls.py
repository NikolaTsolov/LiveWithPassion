from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from .views import login_view, register_view, logout_view

urlpatterns = [
    url(r'^login/', login_view, name="login"),
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', logout_view, name='logout'),
]