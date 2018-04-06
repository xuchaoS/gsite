from django.contrib import admin
from .models import Api, TestCase, TestSuite

# Register your models here.

admin.site.register(Api)
admin.site.register(TestSuite)
admin.site.register(TestCase)

