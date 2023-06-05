from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class ad(models.Model):
    ad_link = models.CharField(max_length=400, unique=True)
    brand = models.CharField(max_length=200,default='')
    model = models.CharField(max_length=200,default='')
    mileage = models.CharField(max_length=200,default='')
    year = models.CharField(max_length=200,default='')
    platform = models.CharField(max_length=200,default='')
    gearbox = models.CharField(max_length=200,default='')
    fuel = models.CharField(max_length=200,default='')
    price=models.CharField(max_length=200,default='')
    fh=models.CharField(max_length=200,default='')
    fiscal_power=models.CharField(max_length=200,default='')


    def __str__(self):
        return self.ad_link