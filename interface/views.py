from django.shortcuts import render, redirect, Http404
from django.contrib.auth.decorators import login_required
from .forms import ApiForm
from .models import Api

# Create your views here.

@login_required
def testcase(request):
    return render(request, 'testcase.html')

@login_required
def api_management(request):
    keyword = request.GET.get('keyword', '')
    apis = Api.objects.filter(name__contains=keyword)
    return render(request, 'api_management.html', {'apis': apis, 'keyword': keyword})

@login_required
def add_api(request):
    if request.method == 'GET':
        form = ApiForm()
        return render(request, 'api_add.html', {'form': form})
    form = ApiForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('api_management')
    else:
        return render(request, 'api_add.html', {'form': form})

@login_required
def edit_api(request, id):
    api = Api.objects.get(id=id)
    if request.method == 'GET':
        form = ApiForm(instance=api)
        return render(request, 'api_edit.html', {'form': form})
    form = ApiForm(request.POST, instance=api)
    if form.is_valid():
        form.save()
        return redirect('api_management')
    else:
        return render(request, 'api_edit.html', {'form': form})

@login_required
def del_api(request, id):
    if request.method != 'POST':
        raise Http404
    if id != int(request.POST.get('id', '0')):
        raise Http404
    Api.delete(Api.objects.get(id=id))
    return redirect('api_management')


