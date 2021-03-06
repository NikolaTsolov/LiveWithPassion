from django.shortcuts import render, get_object_or_404

from .models import Comment
from .forms import CommentForm

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

def comment_thread(request, id):
    obj = get_object_or_404(Comment, id=id)

    initial_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id,
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

    context = {
        "comment": obj,
        "comment_form": comment_form
    }

    return render(request, "comment_thread.html", context)
