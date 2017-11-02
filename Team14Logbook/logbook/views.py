from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Post #, Category
from .forms import PostForm

# def list_of_logbook_by_category(request, category_slug):
#     categories = Category.objects.all()
#     post = Post.objects.filter(status='published')
#
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         post = post.filter(category=category)
#
#     template = 'logbook/list_of_logbook_by_category.html'
#     context = {
#         'categories': categories,
#         'post': post,
#         'category': category,
#     }
#     return render(request, template, context)

@login_required(login_url='/login/')
def logbook_create(request):
    if not request.user.is_authenticated():
        raise Http404

    # if not request.user.is_authenticated():
    #     raise Http404

    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "logbook_form.html", context)

def logbook_detail(request, slug=None): # retrieve
    instance = get_object_or_404(Post, slug=slug)

    if instance.draft:
        if not request.user.is_authenticated():
            if not request.user.is_staff or not request.user.is_superuser:
                raise Http404

    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "logbook_detail.html", context)

def logbook_list(request): # list items
    queryset_list = Post.objects.active()

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get('q')

    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(category__icontains=query)
                ).distinct()

    paginator = Paginator(queryset_list, 10) # Show 10 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "Logbook Entries",
        "page_request_var": page_request_var,

    }
    return render(request, "logbook_list.html", context)

@login_required(login_url='/login/')
def logbook_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)

    if not request.user.get_full_name == instance.user.get_full_name:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404


    form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Item Saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "logbook_form.html", context)

def logbook_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)

    if not request.user.get_full_name == instance.user.get_full_name:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("logbook:logbook_list")
