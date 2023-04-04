from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Book
from .forms import CommentForm, BookForm
from django.shortcuts import get_object_or_404, redirect

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    template_name = "books/book_list.html"
    context_object_name = "books"


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"
    extra_context = {'book_form': CommentForm()}

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=self.kwargs['pk'])
        if request.method=="POST":
            book_form = CommentForm(request.POST)
            if book_form.is_valid():
                new_comment = book_form.save(commit=False)
                new_comment.book = self.book
                new_comment.user = request.user
                new_comment.save()
                return redirect('book_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    template_name = "books/book_create.html"
    fields = ["title", "author", "description", "price", "cover"]
    success_url = reverse_lazy("book_list")

    def dispatch(self, request, *args, **kwargs):
        if request.method=="POST":
            book_form = BookForm(request.POST, request.FILES)
            if book_form.is_valid():
                new_book = book_form.save(commit=False)
                new_book.user = request.user
                new_book.save()
                return redirect('book_list')
        return super().dispatch(request, *args, **kwargs)


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    template_name = "books/book_update.html"
    fields = ["title", "author", "description", "price", "cover"]

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Book
    template_name = "books/book_delete.html"
    success_url = reverse_lazy("book_list")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
