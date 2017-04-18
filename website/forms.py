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
			"year": _("Year of Passing"),
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
