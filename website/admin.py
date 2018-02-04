from django.contrib import admin
from website.models import *
from website.forms import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.core.urlresolvers import reverse

class AlumniCardResource(resources.ModelResource):
	class Meta:
		model = AlumniCard

class SubscriberResource(resources.ModelResource):
	class Meta:
		model = Subscriber
		fields=('id', 'email',)

class AlumniCardAdmin(ImportExportModelAdmin):
	resource_class = AlumniCardResource

class SubscriberAdmin(ImportExportActionModelAdmin):
	list_display = ('email','is_subscribed')
	list_filter = ('is_subscribed',)
	resource_class = SubscriberResource

class EmailMessageAdmin(admin.ModelAdmin):
	list_display = ('subject','created_on','send_url_field' )
	def send_url_field(self, obj):
		return '<a href="%s">%s</a>' % (reverse('website:sendmsg', kwargs={'id':obj.id,}),'Send All',)
	send_url_field.allow_tags = True
	send_url_field.short_description = 'Send all'
	

admin.site.register(Node)
admin.site.register(Event)
admin.site.register(News)
admin.site.register(Link)
admin.site.register(File)
admin.site.register(PhotoSlider)
admin.site.register(DistinguishedAlumniNominator)
admin.site.register(DistinguishedAlumniNominee)
admin.site.register(AlumniCard,AlumniCardAdmin)
admin.site.register(Subscriber,SubscriberAdmin)
admin.site.register(EmailMessage,EmailMessageAdmin)
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
