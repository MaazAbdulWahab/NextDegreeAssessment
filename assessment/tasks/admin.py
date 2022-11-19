from django.contrib import admin
from tasks.models import *
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'status']
    
    search_fields = ['user__username', 'user__email','title']
    raw_id_fields = ['user',]


admin.site.register(Task, TaskAdmin)
