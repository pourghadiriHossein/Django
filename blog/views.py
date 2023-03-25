from django.urls import reverse_lazy
from django.views import generic
from .forms import PostForm
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-datetime_modified')

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post' 

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'blog/new_post.html'

class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post 
    form_class = PostForm
    template_name = 'blog/update_post.html'
    login_url = 'login'

class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('posts_list')

