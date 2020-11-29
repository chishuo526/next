from django.db import models

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    uphone = models.CharField(max_length=11,default=None)


    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
