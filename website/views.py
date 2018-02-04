from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage as EmailMsg, get_connection
from datetime import datetime
from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from website.models import *
from website.forms import *
import calendar
import datetime
# Create your views here.

def samp_index(request):
  context = {
    'message':"Welcome to Student Alumni Mentorship Programme",
  }
  return render(request,'website/samp_index.html',context)

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

##################################################################
def alumnicard(request):
  mTabs = load_nodes(0,None)
  if request.method == "POST":
    alumniform = AlumniCardForm(request.POST,request.FILES)
    if alumniform.is_valid():
      form = alumniform.save()
      form.save()
      context = {
        'form' : alumniform,
      }
      try:
        #Sending Acknowledgement Email
        text = render_to_string('website/alumnicardacknowledgement.html',context=context)
        mail = EmailMsg('Received Request for joining Alumni Association, IIT Roorkee',text,'iitr_daa@iitr.ac.in',['membershipcard.iitraa@gmail.com','iitraa@gmail.com','alumnicell.iitr@gmail.com'])
        photo = form.photo.read()
        sign = form.photo_sign.read()
        degree = form.photo_degree.read()
        mail.attach(form.photo.name, photo)
        mail.attach(form.photo_sign.name, sign)
        mail.attach(form.photo_degree.name,degree)
        mail.send()
      except:
        print("MAIL NOT SENT")
        pass
      context = {
        'mTabs': mTabs,
        'success' : True
      }
      return render(request,'website/alumnicardform.html',context)
    else:
      errors = alumniform.errors
      context = {
        'mTabs': mTabs,
        'alumniform' : alumniform,
        'success' : False,
        'errors' : errors,
      }
      return render(request,'website/alumnicardform.html',context)
  else:
    alumniform = AlumniCardForm()
    context = {
      'mTabs': mTabs,
      'alumniform' : alumniform,
      'success' : False
    }
  return render(request,'website/alumnicardform.html',context)

##########################################################################
##########################################################################


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
      mail = EmailMsg('Nomination for DAA received',text,'iitr_daa@iitr.ac.in',[form.nominee_email,form2.nominator_email,'dora@iitr.ac.in','nikhilsheoran96@gmail.com'])
      nominee_photo = form.nominee_photo.read()
      nominee_resume = form.nominee_resume.read()
      mail.attach(form.nominee_photo.name, nominee_photo)
      mail.attach(form.nominee_resume.name, nominee_resume)
      if form.nominee_optional1:
        nominee_optional = form.nominee_optional1.read()
        mail.attach(form.nominee_optional1.name, nominee_optional)
      mail.send()

      #Sending Details Mail
      text = render_to_string('website/mail.html',context=context)
      mail = EmailMsg('Distinguished Alumni Application',text,'iitr_daa@iitr.ac.in',['dora@iitr.ac.in','nikhilsheoran96@gmail.com'])
      mail.attach(form.nominee_photo.name, nominee_photo)
      mail.attach(form.nominee_resume.name, nominee_resume)
      if form.nominee_optional1:
        mail.attach(form.nominee_optional1.name, nominee_optional)
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
from django.core.validators import validate_email
import uuid
def index(request):
  message = ''
  if request.method == "POST":
    email = request.POST.get('email','')
    try:
      validate_email(email)
      key = uuid.uuid1().hex
      try:
        existing = Subscriber.objects.get(email=email)
        existing.is_subscribed = True
        existing.save()
        message = "Email successfully subscribed"
      except:
        try:
          obj = Subscriber.objects.create(email=email,subscription_key=key)
          message = "Email successfully subscribed"
        except:
          message = "Invalid email address"
    except:
      message = 'Invalid email address'
#    return HttpResponse(message) 
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
    'message':message,
  }
  return render(request,'website/index.html',context)

from django.contrib.sites.shortcuts import get_current_site

def unsubscribe(request,key):
  message = ''
  try:
    subscriber = Subscriber.objects.get(subscription_key=key)
    subscriber.is_subscribed = False
    subscriber.save()
    mail_subject = 'Unsubscribe to AlumniIITR'
    current_site = get_current_site(request)
    text = render_to_string('website/unsubscribe.html', {
                'domain':current_site.domain,
                'sub': subscriber,
            })
    to_email = subscriber.email
    email = EmailMsg(mail_subject, text, to=[to_email])
    email.content_subtype = 'html'
    email.send()
    message = 'Unsubscribed successfully'
  except:
    message = 'Invalid Subscription key'
  return render(request, 'website/sub-unsub.html', {'message':message, }) 

def resubscribe(request,key):
  message = ''
  try:
    subscriber = Subscriber.objects.get(subscription_key=key)
    subscriber.is_subscribed = True
    subscriber.save()
    mail_subject = 'Resubscribe to AlumniIITR'
    current_site = get_current_site(request)
    text = render_to_string('website/resubscribe.html', {
                'domain':current_site.domain,
                'sub': subscriber,
            })
    to_email = subscriber.email
    email = EmailMsg(mail_subject, text, to=[to_email])
    email.content_subtype = 'html'
    email.send()
    message = 'Subscribed successfully'
  except:
    message = 'Invalid Subscription key'
  return render(request, 'website/sub-unsub.html', {'message':message, })  

def send_mail(request,id):
  message = get_object_or_404(EmailMessage, pk=id)
  subscribers = Subscriber.objects.filter(is_subscribed=True)
  mail_subject = message.subject
  current_site = get_current_site(request)
  my_host = 'smtp.gmail.com'
  my_port = 587
  my_use_tls = True
  form = UserForm()
  success=False
  if request.method == "POST":
    form = UserForm(request.POST)
    if form.is_valid():
      my_username = form.cleaned_data['email']
      my_password = form.cleaned_data['password']
      connection = get_connection(host=my_host, 
                            port=my_port, 
                            username=my_username, 
                            password=my_password, 
                            use_tls=my_use_tls)
      connection.open()
      for sub in subscribers:
        text = render_to_string('website/msg.html', {
                'domain':current_site.domain,
                'sub': sub,
                'msg': message,
            })
        to_email = sub.email
        email = EmailMsg(mail_subject, text, to=[to_email], connection=connection)
        email.content_subtype = 'html'
        email.send()
      connection.close()  
      success = True
  context = {
            'userform'  : form,
            'success' : success,
        }
  return render(request, 'website/mailform.html', context)     

def update_profile(request, key):
    """update the subscriberprofile"""
    try:
      user = Subscriber.objects.get(subscription_key=key)
    except:
      message = 'Invalid Subscription key'
      return HttpResponse(message)
    if request.method == 'POST':
        userform = SubscriberForm(request.POST, instance=user)
        message = 'Successfully Updated'
        if userform.is_valid():
            userform.save()
            message = 'successfully updated'
        context = {
            'userform' : userform,
            'message' : message,
        }   
        return render(request, 'website/editProfile.html', context) 
    else:    
        userform = SubscriberForm(instance=user)
        context = {
            'userform'  : userform,
        }
        return render(request, 'website/editProfile.html', context)  