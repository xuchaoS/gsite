#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
File Name: forms
Author: shangxc
Created Time: 2018/4/6 下午3:24
"""
from django import forms
from .models import Api


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
                'class': 'form-control'
            }),
            'note': forms.Textarea(attrs={
                'placeholder': '请输入备注',
                'class': 'form-control'
            }),
        }


if __name__ == '__main__':
    pass
