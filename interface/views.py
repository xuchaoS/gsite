from django.shortcuts import render, redirect, Http404, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ApiForm, SuiteForm, CaseForm
from .models import Api, TestCase, TestSuite
import requests
import json
import traceback


# Create your views here.

@login_required
def case_management(request):
    suite_id = request.GET.get('suite', '')
    case_id = request.GET.get('case', '')
    if request.method == 'GET':
        case = None
        suite = None
        if case_id:
            case = TestCase.objects.get(id=case_id)
        if suite_id:
            suite = TestSuite.objects.get(id=suite_id)
        data = _gen_case_index_data(suite=suite, case=case)
        return render(request, 'case.html', data)
    else:
        case = TestCase.objects.get(id=case_id)
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
        data = _gen_case_index_data(case=case, form=form)
        return render(request, 'case.html', data)


def _gen_case_index_data(suite=None, case=None, data=None, form=None):
    apis = Api.objects.all()
    if not isinstance(data, dict):
        data = {}
    data['apis'] = apis
    data['suite_list'] = TestSuite.objects.all()
    if case:
        data['case'] = case
        suite = case.suite
        data['suite'] = suite
        if form:
            data['form'] = form
        else:
            form = CaseForm(instance=case)
            data['form'] = form
    else:
        data['form'] = CaseForm()
        if suite:
            data['suite'] = suite
    return data


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
    if request.method == 'GET':
        return redirect(reverse('case_management') + '?case=%d' % id)
    case = TestCase.objects.get(id=id)
    form = CaseForm(request.POST, instance=case)
    if form.is_valid():
        form.save()
    else:
        data = _gen_case_index_data(case=case, form=form)
        return render(request, 'case.html', data)
    return redirect(reverse('case_management') + '?case=%d' % id)


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
    result, trace, msg = _exec_case(id)
    case = TestCase.objects.get(id=id)
    data = {
        'result': '执行成功' if result else '执行失败',
        'trace': '\n'.join(trace),
        'msg': '\n' + msg
    }
    data = _gen_case_index_data(case=case, data=data)
    return render(request, 'case.html', data)


def _exec_case(case):
    if not isinstance(case, TestCase):
        case = TestCase.objects.get(id=case)
    content = json.loads(case.content)
    trace = []
    result = False
    i = 0
    try:
        for i, step in enumerate(content):
            trace.append('步骤 %d:' % (i + 1))
            api = step['api']
            path = step['path']
            header = step['header']
            data = step['data']
            expect = step['expect']
            api = Api.objects.get(name=api)
            api_path = json.loads(api.paths)[path]
            url = 'http://%s:%d%s' % (api.ip, api.port, api_path['path'])
            trace.append('\turl: %s' % url)
            method = api_path['method'].lower()
            trace.append('\tmethod: %s' % method)
            if method == 'get':
                res = requests.get(url, data, headers=header)
            elif method == 'post':
                res = requests.post(url, data, headers=header)
            else:
                trace.append('\tFAIL 不支持的method: ' + method)
                break
            trace.append('\tdata: %s' % data)
            trace.append('\texpect: %s' % expect)
            trace.append('\tstatus_code: %s' % res.status_code)
            if res.status_code != 200:
                trace.append('\tFAIL 返回码不是200: %s %s url=%s' % (res.status_code, res.reason, res.url))
                result = False
                break
            trace.append('\tactual: %s' % res.json())
            actual = res.json()
            result = _assert_result(expect, actual, trace)
            if not result:
                break
            trace.append('步骤 %d 完成' % (i + 1))
    except Exception as e:
        trace.append(traceback.format_exc())
    return result, trace, '' if result else '在第 %d 步失败' % (i + 1)


def _assert_result(expect, actual, trace=None):
    success = True
    if isinstance(expect, list) and isinstance(actual, list):
        if len(expect) != 0:
            if len(expect) > len(actual):
                trace.append('\tFAIL: 预期元素个数: %d, 实际元素个数: %d ' % (len(expect), len(actual)))
                success = False
            elif (isinstance(expect[0], list) and isinstance(actual[0], list)) or \
                    (isinstance(expect[0], dict) and isinstance(actual[0], dict)):
                for expect_item in expect:
                    trace.append('\t期望 %s 包含在 %s 中' % (expect_item, actual))
                    for actual_item in actual:
                        if _assert_result(expect_item, actual_item, trace):
                            break
                    else:
                        trace.append('\tFAIL %s 不包含在 %s 中' % (expect_item, actual))
                        success = False
            else:
                for expect_item in expect:
                    trace.append('\t期望 %s 包含在 %s 中' % (expect_item, actual))
                    for actual_item in actual:
                        if expect_item == actual_item:
                            break
                    else:
                        trace.append('\tFAIL %s 不包含在 %s 中' % (expect_item, actual))
                        success = False
    elif isinstance(expect, dict) and isinstance(actual, dict):
        for key, value in expect.items():
            trace.append('\tkey: %s, 预期: %r, 实际: %r' % (key, value, actual[key] if key in actual else ''))
            if key not in actual:
                trace.append('\tFAIL key %s 不包含在 %s 中' % (key, actual))
                success = False
            elif type(value) != type(actual[key]):
                trace.append('\tFAIL 类型不匹配 expect: %r, actual: %r' % (value, actual[key]))
                success = False
            elif isinstance(value, list):
                if not _assert_result(value, actual[key], trace):
                    success = False
            elif isinstance(value, dict):
                if not _assert_result(value, actual[key], trace):
                    success = False
            else:
                if value != actual[key]:
                    trace.append('\tFAIL 不符合预期 expect: %s, actual: %s' % (value, actual[key]))
                    success = False
    else:
        success = False
    return success


@login_required
def exec_suite(request, id):
    suite = TestSuite.objects.get(id=id)
    cases = TestCase.objects.filter(suite=suite)
    success = []
    failed = []
    for case in cases:
        result, trace, msg = _exec_case(case)
        if result:
            success.append(case.name)
        else:
            failed.append(case.name)
    data = {
        'suite': suite,
        'success': success,
        'failed': failed,
        'rate': '%.2f%%' % (len(success) * 100 / (len(success) + len(failed)))
    }
    return render(request, 'suite_result.html', data)



def test(request, type):
    try:
        ret = {'err_code': 0}
        if type == 'sum':
            a = int(request.GET.get('a'))
            b = int(request.GET.get('b'))
            r = a + b
            ret['result'] = r
        elif type == 'list':
            ret['result'] = [i for i in request.GET.values()]
        elif type == 'dict':
            ret['result'] = {i: j for i, j in request.GET.items()}
        rep = HttpResponse(json.dumps(ret).encode())
    except Exception:
        return HttpResponse(b'{"err_code": -1}')
    return rep
