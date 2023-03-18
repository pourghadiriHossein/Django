# Learn Template Tags in Blog Project

## <a href="https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#built-in-filter-reference">Template Tags Refrence</a>

## Create templatetags Folder in blog app
- ### Create __init__.py file in templatetags Folder
- ### Create my_tags.py file in templatetags Folder
- ### Add Two Def in my_tags.py file
```bash
from django import template

register = template.Library()

@register.filter
def add_poulstar(value):
    return f"Poulstar: {value}"


@register.filter
def add_something(value, something):
    return f"{something}: {value}"
```

## Update post_delete_view Function in blog app views.py Files
```bash
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        post.delete()
        return redirect('posts_list')
    return render(request, 'blog/delete_post.html', { 'post': post })
```

## Update post text by template tags in posts_list.html
- ### add load tags in html file
```bash
{% load my_tags %}
```
- ### Use one of Sample Code for post text
```bash
{% comment %} {{ post.text | truncatewords:2 }} {% endcomment %}
{% comment %} {{ post.text| upper }} {% endcomment %}
{% comment %} {{ post.text| lower }} {% endcomment %}
{% comment %} {{ post.text | capfirst }} {% endcomment %}
{% comment %} {{ post.text | title }} {% endcomment %}
{% comment %} {{ post.text | wordcount }} {% endcomment %}
{% comment %} {{ post.text | linebreaks }} {% endcomment %}
{% comment %} {{ post.text | linebreaksbr }} {% endcomment %}

{% comment %} {{ post.text | random }} {% endcomment %}
{% comment %} {{ post.text | slugify }} {% endcomment %}
{% comment %} {{ post.text | add:"2" }} {% endcomment %}
{% comment %} {{ post.text | cut:" " }} {% endcomment %}

{% comment %} {{ post.text | add_poulstar }} {% endcomment %}
{% comment %} {{ post.text | add_something:'hello' }} {% endcomment %}
```

## Create delete_post.html in blog app templates Folder
```bash
{% extends '_base.html' %}

{% block title %}
Delete Post
{% endblock title %}

{% block content %}

<div class='container'>
    <div class="card shadow my-5 mx-2 p-5">
        <h1>
            Delete Post?
        </h1>
        <p>
            Are You sure you want to delete post {{ post.title }} permanently?
        </p>
        <form method="POST" action="{% url 'delete' post.id %}">
            {% csrf_token %}
            <input class="btn btn-danger" type="submit" value="Yes, Delete.">
            <a class="btn btn-info" href="{% url 'post_detail' post.id %}">No, Back to Post Detail of post</a>
        </form>
    </div>
</div>

{% endblock content %}
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
