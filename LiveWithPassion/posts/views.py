from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from urllib import quote_plus

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.db.models import Q


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from .models import Post
from comments.forms import CommentForm
from .forms import PostForm

def post_create(request):
    if not request.user.is_authenticated():
        return redirect("accounts:login")
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfuly Created")

        return HttpResponseRedirect(instance.get_absolute_url())

    contex = {
        "form": form
    }

    return render(request, "posts/post_create.html", contex)  

def post_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser and not request.user.is_authenticated():
        return redirect("accounts:login")
    post = get_object_or_404(Post, slug=slug)

    if post.user.username == request.user.username:
        form = PostForm(request.POST or None, request.FILES or None, instance=post)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "<a href='#'>Item</a> Saved", extra_tags="html_safe")
            
            return HttpResponseRedirect(instance.get_absolute_url())

        contex = {
            "title": post.title,
            "post": post,
            "form": form
        }

        return render(request, "posts/post_update.html", contex)

    return redirect("posts:list")


def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publishDate > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(post.content)

    initial_data = {
            "content_type": post.get_content_type,
            "object_id": post.id,
    }

    comment_form = CommentForm(request.POST or None, initial=initial_data)

    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                            user=request.user,
                            content_type=content_type,
                            object_id=obj_id,
                            content=content_data,
                            parent=parent_obj,
        )



        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = post.comments

    contex = {
        "title": post.title,
        "post": post,
        "share_string": share_string,
        "comments": comments,
        "comment_form": comment_form,
    }

    return render(request, "posts/detail.html", contex)   

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()#.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()

    paginator = Paginator(queryset_list, 3) # Show 25 contacts per page
    page_request_var = 'page'

    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    contex = {
        "title": "LiveWithPassion",
        "posts": queryset,
        "page_request_var": page_request_var,
        "today": today
    }

    return render(request, "posts/post_list.html", contex)

def post_delete(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser and not request.user.is_authenticated():
        return redirect("accounts:login")
    post = get_object_or_404(Post, slug=slug)
    if post:
        if post.user.username == request.user.username:
            post.delete()
            messages.success(request, "Successfuly Deleted")
        raise Http404

    return redirect("posts:list")



def listing(request):
    contact_list = Contacts.objects.all()
    

    return render(request, 'list.html', {'contacts': contacts})