from website.models import *
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django import forms
class DistinguishForm(ModelForm):
	class Meta:
		model = DistinguishedAlumni
		exclude = ()
		labels = {
            "name": _("Name"),
            "dob": _("Date of Birth"),
            "diploma": _("Diploma/Degree obtained from University of Roorkee/IIT Roorkee"),
			"year": _("Year of Graduation"),
			"qualifications": _("Other Qualifications, if any"),
			"address": _("Address for Communication (Including email, fax, phone etc.)"),
			"category": _("Category of Nomination"),
			"description": _("Description of Achievements in the category of Nomination (Limited to 600 Words)"),
			"contribution": _("Details of Contribution to Alma Mater (Limited to 600 Words)"),
			"photo": _("Your Photo"),
			"resume": _("Your Resume"),
			"optional1": _("Optional Certificates"),
			"optional2": _("Optional Certificates"),
			"optional3": _("Optional Certificates"),
        	}
		widgets = {
			'dob' : forms.TextInput(attrs={'placeholder':'MM/DD/YYYY'})
		}

class DistinguishFormNominee(ModelForm):
	class Meta:
		model = DistinguishedAlumniNominee
		exclude = ()
		labels = {
	    "nominee_name": _("Name"),
	"nominee_email":_("Email Address"),
	"nominee_contact":_("Contact No.:"),
	"nominee_degree": _("Degree obtained from University of Roorkee/IIT Roorkee"),
	"nominee_yearpass": _("Year of Graduation"),
	"nominee_quals": _("Other Educational Qualifications, if any"),
	"nominee_address": _("Address"),
	"nominee_designation":_("Designation and Affiliation"),
	"nominee_category":_("Category of Nomination"),
	"nominee_webpage":_("Personal Webpage, if available"),
	"nominee_linkedin":_("LinkedIn Profile Url, if available"),
	"nominee_description":_("Description of achievements in the category of nomination"),
	"nominee_awards":_("Details of Awards Received (Please mention the awarding entity, year and the work leading to the award)"),
	"nominee_photo":_("Recent Photograph (to be uploaded)"),
	"nominee_resume":_("Resume of the nominee (to be uploaded)"),
	"nominee_optional1":_("Any other document you would like to upload"),
		}
		widgets = {
		'nominee_quals':forms.Textarea(attrs={'rows':4}),
		'nominee_address':forms.Textarea(attrs={'rows':4}),
		'nominee_description':forms.Textarea(attrs={'rows':4}),
		'nominee_awards':forms.Textarea(attrs={'rows':4}),
	
	}

class DistinguishFormNominator(ModelForm):
	class Meta:
		model = DistinguishedAlumniNominator
		exclude = ('nominee',)
		labels = {
	"nominator_name": _("Name"),
	"nominator_email":_("Email Address"),
	"nominator_contact":_("Contact No.:"),
	"nominator_designation":_("Designation and Affiliation"),
	"nominator_address":_("Address"),
	"nominator_affiliation":_("Your current or past associations with University of Roorkee/IIT Roorkee"),
	"nominator_moreinfo":_("I can be contacted for more information about the nominee"),
	}
		widgets = {
		'nominator_address':forms.Textarea(attrs={'rows':4}),
		'nominator_affiliation':forms.Textarea(attrs={'rows':4}),
	}
