from django.contrib import admin
from website.models import *
from website.forms import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class AlumniCardResource(resources.ModelResource):
	class Meta:
		model = AlumniCard

class AlumniCardAdmin(ImportExportModelAdmin):
	resource_class = AlumniCardResource

admin.site.register(Node)
admin.site.register(Event)
admin.site.register(News)
admin.site.register(Link)
admin.site.register(File)
admin.site.register(PhotoSlider)
admin.site.register(DistinguishedAlumniNominator)
admin.site.register(DistinguishedAlumniNominee)
admin.site.register(AlumniCard,AlumniCardAdmin)
#class NomineeAdmin(admin.ModelAdmin):
#	exclude = ('nominee_category',)
#	form = DistinguishFormNomineeAdmin
#	list_display = ('nominee_category',)
#	def nominee_category_value(self,instance):
#		return instance.nominee_category
#	nominee_category_value.empty_value_display = '------'
#
#admin.site.register(DistinguishedAlumniNominee,NomineeAdmin)
# Register your models here.
