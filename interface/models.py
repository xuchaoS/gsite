from django.db import models

# Create your models here.


class Api(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    paths = models.TextField(default='{}')
    note = models.TextField(blank=True)

