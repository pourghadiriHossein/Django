from django.shortcuts import render, get_object_or_404
from . import models

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