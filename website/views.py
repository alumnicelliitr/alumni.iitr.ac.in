from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from website.models import *
import calendar
# Create your views here.

def index(request):
  return render(request,'website/index.html')
