from django.db import models

# Create your models here.


class Api(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    paths = models.TextField(default='{}')
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TestSuite(models.Model):
    name = models.CharField(max_length=50, unique=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    name = models.CharField(max_length=50)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)
    content = models.TextField(default='[\n    {\n    }\n]')
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ('name', 'suite')

    def __str__(self):
        return self.name

