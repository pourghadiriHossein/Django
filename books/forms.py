from django.forms import ModelForm
from .models import Comment, Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ("title", "author", "description", "price", "cover")

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields = ('text', 'recommend')