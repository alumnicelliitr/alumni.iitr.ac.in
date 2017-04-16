from django.contrib import admin
from connect.models import *
from django_extensions.admin import ForeignKeyAutocompleteAdmin as ModelAdmin
class AlumniAdmin(ModelAdmin):
  search_fields = ['user__name','user__username']
  related_search_fields = {
    'user':('username',),
  }
admin.site.register(Chat)
admin.site.register(Alumni)#,AlumniAdmin)
admin.site.register(User)
# Register your models here.
