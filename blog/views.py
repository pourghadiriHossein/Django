from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404

def post_list_view(request):
    posts = Post.objects.filter(status='pub')
    context = { 'posts': posts }
    return render(request, 'blog/posts_list.html', context)

def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = { 'post': post }
    return render(request, 'blog/post_detail.html', context)

def post_create_view(request):
    return render(request, 'blog/new_post.html')
