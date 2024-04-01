from django.db import models


class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    tutor = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    specie = models.CharField(max_length=30)
    breed = models.CharField(max_length=20)
    service = models.CharField(max_length=30)
  
    def __str__(self):
        return self.name
