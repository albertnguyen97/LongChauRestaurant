from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from taggit.models import Tag


# Post.objects.filter(publish__year=2022) \
#                   .exclude(title__startswith='Why')
# Create your views here.
# Post.objects.all()
# Post.objects.filter(publish__year=2022)
# Post.objects.order_by('title')
# post = Post.objects.get(id=1)
# post.delete()
# Post.published.filter(title__startswith='Who')

def post_list(request, tag_slug=None):
    posts_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'event.html',
                      {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.objects.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html',
                  {'post': post})
