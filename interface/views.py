from django.shortcuts import render, redirect, Http404, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ApiForm, SuiteForm, CaseForm
from .models import Api, TestCase, TestSuite
import requests
import json


# Create your views here.

@login_required
def case_management(request):
    apis = Api.objects.all()
    data = {'apis': apis}
    data['suite_list'] = TestSuite.objects.all()
    suite_id = request.GET.get('suite', '')
    if suite_id:
        data['suite'] = TestSuite.objects.get(id=int(suite_id))
        case_list = TestCase.objects.filter(suite=data['suite'])
        data['case_list'] = case_list
        case_id = request.GET.get('case', '')
        if case_id:
            case = case_list.get(id=int(case_id))
            data['case'] = case
            if request.method == 'GET':
                form = CaseForm(instance=case)
            else:
                form = CaseForm(request.POST, instance=case)
                if form.is_valid():
                    form.save()
            data['form'] = form
    return render(request, 'case.html', data)


@login_required
def add_case(request):
    if request.method == 'GET':
        if 'suite' in request.GET:
            suite_id = request.GET.get('suite', '')
            suite = TestSuite.objects.get(id=int(suite_id))
            case = TestCase(suite=suite)
            form = CaseForm(instance=case)
        else:
            form = CaseForm()
        apis = Api.objects.all()
        return render(request, 'case_add.html', {'form': form, 'apis': apis})
    form = CaseForm(request.POST)
    if form.is_valid():
        form.save()
        case = TestCase.objects.get(name=form.cleaned_data['name'], suite=form.cleaned_data['suite'])
        return redirect(reverse('case_management') + '?suite=%s&case=%s' % (case.suite.id, case.id))
    else:
        apis = Api.objects.all()
        return render(request, 'case_add.html', {'form': form, 'apis': apis})


@login_required
def edit_case(request, id):
    # case = TestCase.objects.get(id=id)
    # if request.method == 'GET':
    #     form = CaseForm(instance=case)
    #     return render(request, 'case.html', {'form': form})
    # form = CaseForm(request.POST, instance=case)
    # if form.is_valid():
    #     form.save()
    #     return redirect('case')
    # else:
    #     return render(request, 'case.html', {'form': form})
    return case_management(request)


@login_required
def del_case(request, id):
    if request.method != 'POST':
        raise Http404
    if id != int(request.POST.get('id', '0')):
        raise Http404
    case = TestCase.objects.get(id=id)
    TestCase.delete(case)
    return redirect(reverse('case_management') + '?suite=%d' % case.suite.id)


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


@login_required
def suite_management(request):
    keyword = request.GET.get('keyword', '')
    suites = TestSuite.objects.filter(name__contains=keyword)
    return render(request, 'suite.html', {'suites': suites, 'keyword': keyword})


@login_required
def add_suite(request):
    if request.method == 'GET':
        form = SuiteForm()
        return render(request, 'suite_add.html', {'form': form})
    form = SuiteForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('suite_management')
    else:
        return render(request, 'suite_add.html', {'form': form})


@login_required
def edit_suite(request, id):
    suite = TestSuite.objects.get(id=id)
    if request.method == 'GET':
        form = SuiteForm(instance=suite)
        return render(request, 'suite_edit.html', {'form': form})
    form = SuiteForm(request.POST, instance=suite)
    if form.is_valid():
        form.save()
        return redirect('suite_management')
    else:
        return render(request, 'suite_edit.html', {'form': form})


@login_required
def del_suite(request, id):
    if request.method != 'POST':
        raise Http404
    if id != int(request.POST.get('id', '0')):
        raise Http404
    TestSuite.delete(TestSuite.objects.get(id=id))
    return redirect('suite_management')

@login_required
def exec_case(request, id):
    case = TestCase.objects.get(id=id)
    content = json.loads(case.content)
    try:
        for step in content:
            api = step['api']
            path = step['path']
            header = step['header']
            data = step['data']
            expect = step['expect']
            api = Api.objects.get(name=api)
            api_path = json.loads(api.paths)[path]
            url = 'http://%s:%d%s' % (api.ip, api.port, api_path['path'])
            method = api_path['method'].lower()
            if method == 'get':
                res = requests.get(url, data, headers=header)
            elif method == 'post':
                res = requests.post(url, data, headers=header)
            for key, value in expect.items():
                assert res.json()[key] == value
    except Exception as e:
        import traceback
        return HttpResponse(str(traceback.format_exc()).encode() + b'\nfailed')
    else:
        return HttpResponse(b'success')




def test(request):
    try:
        a = int(request.GET.get('a'))
        b = int(request.GET.get('b'))
        r = a + b
        ret = {'result': r, 'err_code': 0}
    except Exception:
        return HttpResponse(b'{err_code: -1}')
    return HttpResponse(json.dumps(ret).encode())
