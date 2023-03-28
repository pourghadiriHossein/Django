from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .forms import BookForm

def book_list_view(request):
    books = models.Book.objects.all()
    context = {
        'books' : books
    }
    return render(request, 'books/book_list.html', context)

def book_detail_view(request, pk):
    book = get_object_or_404(models.Book, pk=pk)
    context = {
        'book' : book
    }
    return render(request, 'books/book_detail.html', context)

def book_create_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=='POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_create.html', { 'form': form } )

def book_update_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('book_list')
    book = get_object_or_404(models.Book, pk=pk)
    if request.method == 'GET':
        form = BookForm(instance=book)
        return render(request, 'books/book_update.html', { 'form': form , 'book': book})
    elif request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')

def book_delete_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    book = get_object_or_404(models.Book, pk=pk)
    if request.method=='POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_delete.html', { 'book': book })  