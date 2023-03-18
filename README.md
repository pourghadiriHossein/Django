# Learn Template Tags in Blog Project

## <a href="https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#built-in-filter-reference">Template Tags Refrence</a>

## Create forms.py in blog app
```bash
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'status']
```

## Import Forms to views.py blog app
```bash
from .forms import PostForm
```

## Update post_create_view function in views.py blog app
```bash
def post_create_view(request):
    if request.method=='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts_list')
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', { 'form': form } )
```

## Update new_post.html templates in blog app
```bash
<form method="POST" action="{% url 'create' %}">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

## Create Update Path on urls.py in blog app
```bash
path('<int:pk>/update/', views.post_update_view, name='update'),
```

## Create post_update_view Function in views.py in blog app
```bash
def post_update_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'blog/update_post.html', { 'form': form , 'post': post})
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts_list')
```

## Update post_detail.html templates in blog app
```bash
<div class="card shadow my-3 p-5">
    <h1>{{ post.title }}</h1>
    <p class="small text-muted mt-2">Created on: {{ post.datetime_created }}</p>
    <p class="mt-2" style="text-align: justify"> {{ post.text }}
    </p>
    <p class="small text-muted">Writer: {{ post.author }}</p>
    <p class="small text-muted mt">Last modified on: {{ post.datetime_modified }}</p>
    <div>
        <a href = "{% url 'update' post.id %}" class="btn btn-sm btn-warning">Update</a>
        <a href = "{% url 'delete' post.id %}" class="btn btn-sm btn-danger">Delete</a>
    </div>
</div>
```

## Create update_post.html templates in blog app
```bash
{% extends '_base.html' %}

{% block title %}
Update Post
{% endblock title %}

{% block content %}

<div class="container mt-4">
    <div class="row">
        <div class="col-9">
            <div class="card shadow my-3 p-5">
                <h3>Update Post:</h3>
                <form method="POST" action="{% url 'update' post.id %}">
                    {% csrf_token %}
                    <table>
                        {{ form.as_table }}
                    </table>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
        <div class="col-3">
            <div class="card my-3 sticky-top">
                <h5 class="card-header">About</h5>
                <div class="card-body">
                    <p class="card-text";>Poulstar is an institute which help children learn
                        different programming languagess. Kids and teenager learn how to
                        code in different programming languages by games and playing.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

{% endblock content %}
```

## Create Delete Path on urls.py in blog app
```bash
path('<int:pk>/delete/', views.post_delete_view, name='delete'),
```

## Create post_delete_view Function in views.py in blog app
```bash
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('posts_list')
```

## Run Your App
- ### In Windows
```bash
py manage.py runserver
```
- ### In MacOS
```bash
python manage.py runserver
```
- ### In Linux
```bash
python3 manage.py runserver
```
