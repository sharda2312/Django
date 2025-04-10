from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
        
class Student(School):
    stuname = models.CharField(max_length=100)
    roll = models.IntegerField()
    
