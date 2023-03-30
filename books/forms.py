from django.forms import ModelForm
from . import models

class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = ['title', 'author', 'description', 'price', 'cover']

class CommentForm(ModelForm):
    class Meta:
        model=models.Comment
        fields = ('text', 'recommend')