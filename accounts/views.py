from django.views import generic
from django.contrib.auth import forms
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class SignUpView(generic.CreateView):
    form_class = forms.UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('posts_list'))

        return super().dispatch(request, *args, **kwargs)
