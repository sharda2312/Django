from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id","name", "email", "is_staff", "is_superuser", 
                    "is_active", "otp","otp_exp", "max_otp_try", "otp_locked_until",
                    ]