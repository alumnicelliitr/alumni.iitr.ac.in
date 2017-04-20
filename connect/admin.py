from django.contrib import admin
from connect.models import *
from django_extensions.admin import ForeignKeyAutocompleteAdmin as ModelAdmin
from django.contrib.auth.models import Group
class AlumniAdmin(ModelAdmin):
  search_fields = ['user__name','user__username']
  related_search_fields = {
    'user':('username',),
  }
admin.site.unregister(Group)
admin.site.register(Chat)
admin.site.register(Alumni)#,AlumniAdmin)
# Register your models here.
