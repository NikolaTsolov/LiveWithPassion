from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import SubmitedURLForm

# Create your views here.

def index(request, *args, **kwargs):
	return HttpResponseRedirect('./templates/home.html')

class HomeView(View):
	def get(self, request, *args, **kwargs):
		the_form = SubmitedURLForm()
		context = {
			"title": "Hey You",
			"form": the_form
		}
		return render(request, 'home.html', context)

	def post(self, request, *args, **kwargs):
		print(request.POST)
		print(request.POST.get("url"))
		form = SubmitedURLForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
		context = {
			"title": "Hey You",
			"form": form
		}
		return render(request, 'home.html', context)