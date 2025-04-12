from django.contrib import admin
from .models import Student, Teacher, Contracter

# Register your models here.

@admin.register(Student)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "roll", "standard"]
    

@admin.register(Teacher)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "salary"]
    

@admin.register(Contracter)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "payment", "date"]