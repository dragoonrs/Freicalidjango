from django.db import models

# Create your models here.
from django.db import models


class igpm(models.Model):
    data = models.DateTimeField('data')
    taxa = models.DecimalField(max_digits=20, decimal_places=10)
    multiplicadorAbsoluto = models.DecimalField(max_digits=20, decimal_places=10)