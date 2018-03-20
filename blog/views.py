import re

from django.forms import ModelForm
from django.http import HttpResponse
from django.template import loader
from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from comments.views import CommentForm
from comments.models import Comment
from .models import Blog, Category
from misc.utils import unique_slugify

def index(request):
    return render_to_response('blog/index.html', {
        'categories': Category.objects.all()[0:15],
        'posts': Blog.objects.all()[:20],
        'user': request.user
    })

def view_post(request, slug):
    comment_form = CommentForm()
    return render_to_response('blog/view_post.html', {
        'post': get_object_or_404(Blog, slug=slug),
        'request': request,
        'comment_form': comment_form,
        'comment_list': Comment.objects.filter(
            object_id=get_object_or_404(Blog, slug=slug).id,
            model='b'
        ),
    })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('blog/view_category.html', {
        'category': category,
        'posts': Blog.objects.filter(category=category)
    })

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ['slug', 'owner']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['slug']

def create_post(request):
    if (Category.objects.count == 0):
        return redirect('/blog/create_category/')
    blog_create_form = BlogForm()
    if request.method == "POST":
        blog_create_form = BlogForm(request.POST)
        if blog_create_form.is_valid():
            post = blog_create_form.save(commit=False)
            unique_slugify(post, post.title)
            post.save()
            return redirect(post)
    template = loader.get_template('blog/create_form.html')
    context = {
        'create_form' : blog_create_form.as_p(),
    }
    return HttpResponse(template.render(context, request))

def create_category(request):
    category_create_form = CategoryForm()
    if request.method == "POST":
        category_create_form = CategoryForm(request.POST)
        if category_create_form.is_valid():
            category = category_create_form.save(commit=False)
            unique_slugify(category, category.title)
            category.save()
            return redirect('/blog/')
    template = loader.get_template('blog/create_form.html')
    context = {
        'create_form' : category_create_form.as_p(),
    }
    return HttpResponse(template.render(context, request))