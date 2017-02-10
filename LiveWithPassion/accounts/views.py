from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

from .forms import UserLoginForm, UserRegistrationForm

def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    template_name = "account/register.html"

    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        return redirect("accounts:login")

    return render(request, template_name, {"form": form}) 



def login_view(request):
    form = UserLoginForm(request.POST or None)
    template_name = "account/login.html"

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
        #if user.is_active:
            login(request, user)
            return redirect("posts:list") 
    return render(request, template_name, {"form": form}) 

def logout_view(request):
    logout(request)
    return redirect("accounts:login") 
