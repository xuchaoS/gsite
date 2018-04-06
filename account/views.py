from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import LoginForm

# Create your views here.


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form, })
    form = LoginForm(request.POST)
    if form.is_valid():
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            return redirect('home')
        else:
            return render(request, 'login.html', {'form': form, 'password_is_wrong': True})
    else:
        return render(request, 'login.html', {'form': form, })

