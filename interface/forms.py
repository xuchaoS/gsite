#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
File Name: forms
Author: shangxc
Created Time: 2018/4/6 下午3:24
"""
from django import forms
from .models import Api, TestCase, TestSuite
import json


def clean_json(field):
    def wrapper(self):
        value = self.cleaned_data[field]
        try:
            j = json.loads(value)
        except json.JSONDecodeError as e:
            raise forms.ValidationError('json格式不正确：%s' % e, code='json')
        return json.dumps(j)
    return wrapper


class ApiForm(forms.ModelForm):
    class Meta:
        model = Api
        fields = ['name', 'ip', 'port', "paths", 'note']
        labels = {'name': '名称', 'ip': 'IP', 'port': '端口', "paths": '接口地址', 'note': '备注'}
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '可供调用的名称',
                'class': 'form-control'
            }),
            'ip': forms.TextInput(attrs={
                'placeholder': '接口IP地址',
                'class': 'form-control'
            }),
            'port': forms.NumberInput(attrs={
                'placeholder': '接口端口号',
                'class': 'form-control'
            }),
            "paths": forms.Textarea(attrs={
                'class': 'form-control format_json'
            }),
            'note': forms.Textarea(attrs={
                'placeholder': '请输入备注',
                'class': 'form-control'
            }),
        }

    clean_paths = clean_json('paths')




class SuiteForm(forms.ModelForm):
    class Meta:
        model = TestSuite
        fields = ['name', 'note']
        labels = {'name': '名称', 'note': '备注'}
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '请输入套件名称',
                'class': 'form-control'
            }),
            'note': forms.Textarea(attrs={
                'placeholder': '请输入备注',
                'class': 'form-control'
            }),
        }


class CaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['suite', 'name', 'content', 'note']
        labels = {'suite': '所属套件', 'name': '名称', 'content': '内容', 'note': '备注'}
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': '请输入用例名称',
                'class': 'form-control'
            }),
            'suite': forms.Select(attrs={
                'class': 'form-control disabled'
            }),
            "content": forms.Textarea(attrs={
                'class': 'form-control format_json'
            }),
            'note': forms.Textarea(attrs={
                'placeholder': '请输入备注',
                'class': 'form-control'
            }),
        }
        error_messages = {'__all__':{'unique_together': '套件中已经存在相同名称的用例'}}

    clean_content = clean_json('content')


if __name__ == '__main__':
    pass
