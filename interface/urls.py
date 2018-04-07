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
    path('', views.case_management, name='interface'),
    path('suite/', views.suite_management, name='suite_management'),
    path('suite/add', views.add_suite, name='suite_add'),
    path('suite/edit/<int:id>', views.edit_suite, name='suite_edit'),
    path('suite/del/<int:id>', views.del_suite, name='suite_del'),
    path('case/', views.case_management, name='case_management'),
    path('case/add', views.add_case, name='case_add'),
    path('case/edit/<int:id>', views.edit_case, name='case_edit'),
    path('case/del/<int:id>', views.del_case, name='case_del'),
    path('api/', views.api_management, name='api_management'),
    path('api/add', views.add_api, name='api_add'),
    path('api/edit/<int:id>', views.edit_api, name='api_edit'),
    path('api/del/<int:id>', views.del_api, name='api_del'),
]
