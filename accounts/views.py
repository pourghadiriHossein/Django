from django.shortcuts import render, redirect
from django.contrib.auth import forms

def sign_up_view(request):
    if request.user.is_authenticated:
        return redirect('posts_list') 
    if request.method=='POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = forms.UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form })