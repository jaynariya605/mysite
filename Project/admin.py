from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Project.models import approvals
# Register your models here.


class Viewapproval(admin.ModelAdmin):
	
	

	list_display = ('id','user', 'date_modified', 'date_published')
admin.site.register(approvals,Viewapproval)