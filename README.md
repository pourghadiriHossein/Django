# Use Login Required in Book Store Project

## Update settings.py File in config folder
```bash
# Email Config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "fake.poulstar@gmail.com"
EMAIL_HOST_PASSWORD = "ftgtgsssfukhiyik"
```

## books app
- ### Update views.py file
```bash
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .forms import BookForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def book_list_view(request):
    books = models.Book.objects.all()
    paginator = Paginator(books, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'books/book_list.html', context)

def book_detail_view(request, pk):
    book = get_object_or_404(models.Book, pk=pk)
    comments = book.comments.all()
    if request.method=="POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'book': book,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'books/book_detail.html', context)

@login_required
def book_create_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=='POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_create.html', { 'form': form } )

@login_required
def book_update_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('book_list')
    book = get_object_or_404(models.Book, pk=pk)
    if request.method == 'GET':
        form = BookForm(instance=book)
        return render(request, 'books/book_update.html', { 'form': form , 'book': book})
    elif request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')

@login_required
def book_delete_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    book = get_object_or_404(models.Book, pk=pk)
    if request.method=='POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_delete.html', { 'book': book })  
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
