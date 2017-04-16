from django import forms
import model_constants as MC
from models import Branch
from taggit.forms import *


branch_list = [(x.code, x.name) for x in Branch.objects.all()]
branch_list.insert(0, ("","Any"))


class AdvancedSearchForm(forms.Form):
  name = forms.CharField(label = "Name", required = False, max_length = MC.TEXT_LENGTH, widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Name'}))
  branch = forms.ChoiceField(choices = branch_list, label ="Branch", required = False, widget = forms.Select(attrs = {'class': 'form-control', 'placeholder': 'Branch'}))
  batch = forms.IntegerField(label ="Batch", required = False, min_value = 2010, max_value = 2018, widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Batch'}))
  tags = TagField(label = "Tags", required = False, widget = forms.TextInput(attrs = {'class' : 'form-control', 'placeholder' : 'Tags', 'data-role' : 'tagsinput'}))


class SearchForm(forms.Form):
  tags = TagField(label = "Tags", required = True, widget = forms.TextInput(attrs = {'class' : 'form-control', 'placeholder' : 'Start Typing tags to search ...', 'data-role' : 'tagsinput'}))
