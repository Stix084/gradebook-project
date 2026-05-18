from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User

# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        
        "username",
        "role",
       "student_number", 
       "is_staff"
       
       )
    
    list_filter = ("role",)
    search_fields = ("username", "student_number")






