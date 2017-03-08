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
    if tab.external_url:
      tab.url = tab.external_url
    else:
      try:
        if parent.url:
          tab.url = parent.url + "/" + tab.url_name
        else:
          tab.url = "/" + tab.url_name
      except:
        tab.url = "/" + tab.url_name
    tab.children = load_nodes(level+1,tab)
  return mTabs

def load_level(url_name,level = 0):
  try:
    active = Node.objects.filter(visibility=True,level=level,url_name=url_name).get()
    active.url = "/" + url_name
    active.children = load_nodes(level+1,active)
    return active
  except:
    return None

def level(request,level0,level1 = None,level2 = None):
  mTabs = load_nodes(0,None)
  if level1 == None:
    active = load_level(level0,0)
  elif level2 == None:
    active = load_level(level1,1)
  else:
    active = load_level(level2,2)
  base = load_level(level0,0)
  print base.children
  print base
  print base.url
  print active.children
  print active
  print active.url
  print base.children
  print "yo"
  for child in base.children:
    print child
    print "Chidl : "+str(len(child.children))
  context = {
    'mTabs':mTabs,
    'active':active,
    'base':base,
  }
  return render(request,'website/page.html',context)

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
