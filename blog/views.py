from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def post_list_view(request):
    posts = Post.objects.filter(status='pub')
    context = { 'posts': posts }
    return render(request, 'blog/posts_list.html', context)

def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = { 'post': post }
    return render(request, 'blog/post_detail.html', context)

def post_create_view(request):
    if request.method=='POST':
        title = request.POST['title']
        text = request.POST.get('text')
        user = User.objects.first()
        if title=="salam":
            return render(request, 'blog/new_post.html')
        Post.objects.create(title=title, text=text, status='pub', author=user)
    return render(request, 'blog/new_post.html')