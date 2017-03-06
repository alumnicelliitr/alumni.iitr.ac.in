from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from website.models import *
import calendar
import datetime
# Create your views here.

def load_nodes(level,parent = None):
  mTabs = Node.objects.filter(visibility=True,level=level,parent=parent).order_by('priority')
  for tab in mTabs:
    tab.children = load_nodes(level+1,tab)
  return mTabs

def index(request):
  mTabs = load_nodes(0,None)

  mEvents = Event.objects.filter(visibility=True,expiry_date__gte=datetime.date.today()).order_by('priority')

  mNews = News.objects.filter(visibility=True,expiry__gte=datetime.date.today()).order_by('priority')

  mLinks = Link.objects.filter(visibility=True).order_by('priority')
  context = {
    'mTabs':mTabs,
    'mEvents':mEvents,
    'mLinks':mLinks,
    'mNews':mNews,
  }
  return render(request,'website/index.html',context)
