#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
File Name: forms
Author: shangxc
Created Time: 2018/4/2 下午10:54
"""
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=50,
        label="用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': "用户名",
                'class': 'form-control',
            }
        ),
    )
    password = forms.CharField(
        required=True,
        max_length=50,
        label="密码",
        error_messages={'required': '请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "密码",
                'class': 'form-control',
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()


if __name__ == '__main__':
    pass
