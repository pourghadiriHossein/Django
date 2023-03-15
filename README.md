# Simple Form Data For Save Post


## Update form Tag in new_post.html 
```bash
<form method="POST" action="{% url 'create' %}">
    {% csrf_token %}
    <div class="form-group py-2">
        <label class="py-1">Enter post title</label>
        <input type="text" class="form-control" placeholder="e.g. Some Title" name="title">
    </div>
    <div class="form-group py-2">
        <label class="py-1">Enter post text:</label>
        <textarea class="form-control" name="text" rows="8" placeholder="Enter your post text here..."></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```


## Update post_create_view function for blog app in views.py file
```bash
from django.contrib.auth.models import User

def post_create_view(request):
    if request.method=='POST':
        title = request.POST['title']
        text = request.POST.get('text')
        user = User.objects.first()
        if title=="salam":
            return render(request, 'blog/new_post.html')
        Post.objects.create(title=title, text=text, status='pub', author=user)
    return render(request, 'blog/new_post.html')
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
