from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from connect.models import *
from django.core import serializers

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import model_constants as MC
import json

from .forms import SearchForm, AdvancedSearchForm

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/done')

@login_required
def index(request):
  if request.method == 'POST':
    form = SearchForm(request.POST)
  else:
    form = SearchForm(request.POST)
  return render(request, 'connect/index.html', {'form': form})

@login_required
def advanced(request):
  if request.method == 'POST':
    form = AdvancedSearchForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      branch = form.cleaned_data['branch']
      batch = form.cleaned_data['batch']
      tags = form.cleaned_data['tags']
      query = []
      alumni = Alumni.objects.all()
      if name:
        alumni = alumni.filter(user__name__icontains = name)
        query.append(name)
      if branch:
        alumni = alumni.filter(branch = branch)
        query.append(branch)
      if batch:
        alumni = alumni.filter(passout_year = batch)
        query.append(batch)
      if tags:
        alumni = alumni.filter(tags__name__in = tags).distinct()
        query.append(' '.join(tags))
      if len(query) > 0:
        query  = ','.join(query)
        context = {
          'query': query,
          'form': form,
          'alumni': alumni
        }
        return render(request, 'connect/search-results.html', context)
    else:
      context = {
        'form': form
      }
      return render(request, 'connect/advanced.html', {'form':form})
  else:
    form = AdvancedSearchForm()
  return render(request,'connect/advanced.html',{'form':form})

def ajax_tag_search(request):
  if request.method == 'POST':
    form = SearchForm(request.POST)
    if form.is_valid():
      tags = form.cleaned_data['tags']
      alumni_q = Alumni.objects.filter(tags__name__in = tags).distinct()
      alumni = serializers.serialize("json", alumni_q)
      return JsonResponse(alumni)
#def chat(request,receiver = None):
#    if receiver == None:
        # user = request.user
#        user = User.objects.get(username='14114031')
#        latest = Chat.objects.filter(user = user).order_by('-datetime_created')[0]
#        return HttpResponseRedirect('/chat/t/'+latest.other_user.username)
#    else:
#        user = User.objects.get(username='14114031')
#        latest = Chat.objects.filter(user = user).order_by('-datetime_created')[:10]
#        context = {
#           'active' : user,
#            'chat_users' : latest,
#        }
#        return render(request,'connect/chat.html',context)
        #One highlighted user
        #List of latest users on left
        #If highlighted matches any on left. cool =D

@csrf_exempt
def chat_alumni(request, chat_ekey):
    try:
      chat_request = ChatRequest.objects.get_by_ekey(chat_ekey)
      if request.user:
        logout(request)
      owner = chat_request.receiver
      user = authenticate(username=owner.username,password='helloiitr')
      if user is not None:
        if user.is_active:
          login(request,user)
          return redirect("/connect/student_chat/" + chat_request.sender.username)
        else:
          redirect("/")
      else:
        redirect("/")
    except Exception as e:
      print e
      return HttpResponse('Not a valid link')


@csrf_exempt
@login_required
def chat_request_view(request):
    try:
        student = Student.objects.get(user=request.user)
    except:
        return JsonResponse({"done":False, "message":"You're not a student"})
    try:
        alumni_id = request.POST.get("alumni_id")
        alumni = Alumni.objects.get(id=alumni_id)
    except:
        return JsonResponse({"done":False, "message":"Alumni with given id does not exist."})

    chat_request, created = ChatRequest.objects.get_or_create(sender=request.user, receiver=alumni.user)
#    if not created:
#        return JsonResponse({"done":False, "message":"You have already requested from this alumni"})
    send_mail('Mail from alum portal', "You're requested to chat with "+student.user.name+" go to url : "+"http://192.168.121.187:6969/connect/chat_alumni/"+chat_request.ekey+"/", 'img@channeli.in', [alumni.email])
    return JsonResponse({"done":True, "message":"Email has been sent."})

@csrf_exempt
@login_required
def add_message(request):
  try:
    sender = request.user
    receiver = User.objects.get(username=request.POST.get('target',''))
    message = request.POST.get('message','')
    c = Chat.objects.create(sender = sender, receiver = receiver, message = message)
    c.save()
    chat_request, created = ChatRequest.objects.get_or_create(sender=sender, receiver=receiver)
    if created:
      send_mail('Mail from alum portal', "You're requested to chat with "+sender.name+". Go to the URL : "+"http://192.168.121.187:63000/connect/chat_alumni/"+chat_request.ekey+"/", 'img@channeli.in', ['nikhilsheoran96@gmail.com']) #alumni.email])
    return HttpResponse('success')
  except Exception as e:
    print e
    return HttpResponse('error')

def messages(request,rcvr):
  receiver = User.objects.get(username = rcvr)
  user = request.user
  messages= Chat.objects.filter(Q(sender = user, receiver = receiver) | Q(sender = receiver, receiver = user)).order_by('-datetime_created')[:30]
  return render(request, 'connect/chat.html',{'messages':messages,'user':user,'receiver':receiver})

@login_required
def student_chat(request,target = None):
  if target == None:
    user = request.user
    try:
      messages = Chat.objects.filter(Q(sender = user) | Q(receiver = user)).order_by('-datetime_created')[0]
      receiver = messages.receiver.username if (messages.sender == user) else messages.sender.username
      return redirect('/connect/student_chat/'+receiver)
    except Exception as e:
      print e
      #Person hasn't chatted with anyone and is opening /student_chat/
      context = {
        'empty': True,
        'user' : user,
      }
      return render(request,'connect/chat.html',context)
  else:
    user = request.user
    messageList = Chat.objects.filter(Q(sender = user) | Q(receiver = user)).order_by('-datetime_created')
    userList = []
    for message in messageList:
      if message.sender == user and message.receiver not in userList:
        userList.append(message.receiver)
      elif message.receiver == user and message.sender not in userList:
        userList.append(message.sender)
    target = User.objects.get(username=target)
    messages = Chat.objects.filter(Q(sender = user, receiver = target) | Q(receiver = user, sender = target)).order_by('-datetime_created')
    first = False
    if(len(messages) == 0):
      first = True
    context = {
    'empty' : False,
    'first' : first,
    'messages' : messages,
    'user' : user,
    'target' : target,
    'userList' : userList
    }
  return render(request, 'connect/chat.html',context)

@csrf_exempt
def chat_list(request):
  alumni_id = request.POST.get("alumni_id")
  student_id = request.POST.get("student_id")
  alumni_user = User.objects.get(username = alumni_id)
  student_user = User.objects.get(username = student_id)
  try:
    messages = Chat.objects.filter(Q(sender = student_user, receiver = alumni_user) | Q(sender = alumni_user, receiver = student_user)).order_by('-datetime_created')
    message = serializers.serialize('json', messages, fields=('message','sender','receiver'))
  except:
    messages = []
  return JsonResponse(message,safe=False)

@csrf_exempt
def chat_user_list(request):
  user = User.objects.get(username=request.POST.get("enrollment_no"))
  chats = Chat.objects.filter(Q(sender = user) | Q(receiver = user))
  users = map(lambda chat: chat.sender if chat.receiver == user else chat.receiver, chats)
  users_set = set(users)
  users_list = list(users_set)
  print users_list
  data = []
  for user in users_list:
    try:
      alumnus = Alumni.objects.get(user = user)
      if alumnus:
        element = {"id":user.id, "username":user.username, "name":user.name, "photo": user.photo, "branch":alumnus.branch.name, "admission_year":alumnus.admission_year, "passout_year":alumnus.passout_year,"type":"alumnus"}
    except:
      pass
    try:
      student = Student.objects.get(user = user)
      if student:
        element = {"id":user.id, "username":user.username, "name":user.name, "photo": user.photo, "branch":student.branch.name, "admission_year":student.admission_year, "bhawan":student.bhawan,"type":"student"}
    except:
      pass
    data.append(element)
  return JsonResponse(data, safe=False)


