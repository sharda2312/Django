from django.db import models

# Create your models here.

"""
class student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    roll = models.IntegerField()
    standard = models.IntegerField()
    
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    salary = models.IntegerField()
    date = models.DateField()
    
class contracter(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    payment = models.IntegerField()
    date = models.DateTimeField()
    
"""

# This above models can be made more intuitive using Abstract inheritance

class CommondField(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    date = models.DateField()
    class Meta:
        abstract = True
        
class Student(CommondField):
    roll = models.IntegerField()
    standard = models.IntegerField()
    date = None
    
class Teacher(CommondField):
    salary = models.IntegerField()
    
class Contracter(CommondField):
    payment = models.IntegerField()
    date = models.DateTimeField()