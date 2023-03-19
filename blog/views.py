from django.shortcuts import render, redirect
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import PostForm


def post_list_view(request):
    posts = Post.objects.filter(status='pub')
    context = { 'posts': posts }
    return render(request, 'blog/posts_list.html', context)

def post_detail_view(request, pk): 
    post = get_object_or_404(Post, pk=pk)
    context = { 'post': post }
    return render(request, 'blog/post_detail.html', context)

def post_create_view(request):
    if not request.user.is_authenticated:
        return redirect('posts_list')
    if request.method=='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts_list')
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', { 'form': form } )

def post_update_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('posts_list')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'blog/update_post.html', { 'form': form , 'post': post})
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts_list')

def post_delete_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('posts_list')
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        post.delete()
        return redirect('posts_list')
    return render(request, 'blog/delete_post.html', { 'post': post })  