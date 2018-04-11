from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def machines(request):
    return redirect('machines_list')


def machines_list(request):
    return render(request, 'machines_list.html')
