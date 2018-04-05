from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def testcase(request):
    return render(request, 'testcase.html')

@login_required
def api_management(request):
    return render(request, 'api_management.html')
