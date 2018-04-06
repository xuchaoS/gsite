"""gsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from interface import views

urlpatterns = [
    path('testcase/', views.testcase, name='interface'),
    path('api/', views.api_management, name='api_management'),
    path('api/add', views.add_api, name='api_add'),
    path('api/edit/<int:id>', views.edit_api, name='api_edit'),
    path('api/del/<int:id>', views.del_api, name='api_del'),
]
