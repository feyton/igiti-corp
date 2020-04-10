from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CreateUserForm

from django.contrib.auth import logout, decorators


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    template_name = 'registration/registration.html'
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password1)
            login(request, user)
            return render(request, 'registration/custom.html')
    else:
        form = CreateUserForm()

    return render(request, template_name, {'form':form})
