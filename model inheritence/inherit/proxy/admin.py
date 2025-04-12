from django.contrib import admin
from .models import Student, PStudent

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["id","name","roll", "city"]

@admin.register(PStudent)
class PStudentAdmin(admin.ModelAdmin):
    list_display = ["id","name","roll", "city"]