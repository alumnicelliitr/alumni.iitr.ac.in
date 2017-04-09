from django import forms
import model_constants as MC

class SearchForm(forms.Form):
  name = forms.CharField(label = "Name", max_length = MC.TEXT_LENGTH)
  branch = forms.CharField(label ="Branch", max_length = MC.CODE_LENGTH)
  batch = forms.IntegerField(label ="Batch")

