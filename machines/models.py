from django.db import models

# Create your models here.


class Machine(models.Model):
    name = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    system = models.CharField(max_length=50)
    note = models.TextField(blank=True)