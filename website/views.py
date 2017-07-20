from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from datetime import datetime
from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from website.models import *
from website.forms import *
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
    active = Node.objects.filter(level=level,url_name=url_name).get()
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
  if active == None:
    #try if a page
    return redirect('/')
  context = {
    'mTabs':mTabs,
    'active':active,
    'base':base,
  }
  return render(request,'website/page.html',context)

def distinguishedformnew(request):
  mTabs = load_nodes(0,None)
  if request.method == "POST":
    distinguishForm = DistinguishFormNominee(request.POST,request.FILES)
    distinguishForm2 = DistinguishFormNominator(request.POST)
    if distinguishForm.is_valid() and distinguishForm2.is_valid():
      form = distinguishForm.save()
      form2 = distinguishForm2.save(commit=False)
      form2.nominee = form
      form2.save()
      context = {
        'form' : distinguishForm,
	'form2' : distinguishForm2
      }

      #Sending Acknowledgement Email
      text = render_to_string('website/acknowledgement.html',context=context)
      mail = EmailMessage('Nomination for DAA received',text,'nik17.ucs2014@iitr.ac.in',[form.nominee_email,form2.nominator_email,'nikhilsheoran96@gmail.com'])
      mail.attach(form.nominee_photo.name, form.nominee_photo.read())
      mail.attach(form.nominee_resume.name, form.nominee_resume.read())
      if form.nominee_optional1:
        mail.attach(form.nominee_optional1.name, form.nominee_optional1.read())
      mail.send()

      #Sending Details Mail
      text = render_to_string('website/mail.html',context=context)
      mail = EmailMessage('Distinguished Alumni Application',text,'nik17.ucs2014@iitr.ac.in',['nikhilsheoran96@gmail.com'])
      mail.attach(form.nominee_photo.name, form.nominee_photo.read())
      mail.attach(form.nominee_resume.name, form.nominee_resume.read())
      if form.nominee_optional1:
        mail.attach(form.nominee_optional1.name, form.nominee_optional1.read())
      mail.send()

      context = {
        'mTabs': mTabs,
        'success' : True
      }
      return render(request,'website/distinguishform2.html',context)
    else:
      errors = distinguishForm.errors
      errors2 = distinguishForm2.errors
      context = {
        'mTabs': mTabs,
        'distinguishForm' : distinguishForm,
	'distinguishForm2' : distinguishForm2,
        'success' : False,
        'errors' : errors,
	'errors2' : errors2
      }
      return render(request,'website/distinguishform2.html',context)
  else:
    distinguishForm = DistinguishFormNominee()
    distinguishForm2 = DistinguishFormNominator()
    context = {
      'mTabs': mTabs,
      'distinguishForm' : distinguishForm,
      'distinguishForm2' : distinguishForm2,
      'success' : False
    }
  return render(request,'website/distinguishform2.html',context)

#def distinguishedform(request):
#  mTabs = load_nodes(0,None)
#  if request.method == "POST":
#    distinguishForm = DistinguishForm(request.POST,request.FILES)
#    if distinguishForm.is_valid():
#      form = distinguishForm.save()
#      context = {
#        'form' : distinguishForm,
#      }
#      text = render_to_string('website/mail.html',context=context)
#      print text
#      mail = EmailMessage('Distinguished Alumni Application',text,'nik17.ucs2014@iitr.ac.in',['nikhilsheoran96@gmail.com','daair.iitr@iitr.ac.in'])
#      mail.attach(form.photo.name, form.photo.read())
#      mail.attach(form.resume.name, form.resume.read())
#      if form.optional1:
#        mail.attach(form.optional1.name, form.optional1.read())
#      if form.optional2:
#        mail.attach(form.optional2.name, form.optional2.read())
#      if form.optional3:
#        mail.attach(form.optional3.name, form.optional3.read())
#      mail.send()
#      context = {
#        'mTabs': mTabs,
#        'success' : True
#      }
#      return render(request,'website/distinguishform.html',context)
#    else:
#      errors = distinguishForm.errors
#      context = {
#        'mTabs': mTabs,
#        'distinguishForm' : distinguishForm,
#        'success' : False,
#        'errors' : errors
#      }
#      return render(request,'website/distinguishform.html',context)
#  else:
#    distinguishForm = DistinguishForm()
#    context = {
#      'mTabs': mTabs,
#      'distinguishForm' : distinguishForm,
#      'success' : False
#    }
#  return render(request,'website/distinguishform.html',context)
#

def index(request):
  mTabs = load_nodes(0,None)
  mEvents = Event.objects.filter(visibility=True,expiry_date__gte=datetime.date.today()).order_by('priority')
  mEventsPast = Event.objects.filter(visibility=True,expiry_date__lte=datetime.date.today()).order_by('priority')
  mNews = News.objects.filter(visibility=True,expiry__gte=datetime.date.today()).order_by('priority')
  mLinks = Link.objects.filter(visibility=True).order_by('priority')
  mSlider = PhotoSlider.objects.filter(visibility=True).order_by('priority')
  context = {
    'mTabs':mTabs,
    'mEvents':mEvents,
    'mEventsPast':mEventsPast,
    'mLinks':mLinks,
    'mNews':mNews,
    'mSlider':mSlider,
  }
  return render(request,'website/index.html',context)
