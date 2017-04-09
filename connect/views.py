from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from connect.models import *
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .forms import SearchForm


def index(request):
  if request.method == 'POST':
    form = SearchForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      alumni = Alumni.objects.filter(user__name__contains = name)
      context = {
        'alumni': alumni
      }
      return render(request, 'connect/search.html', context)
  else:
    form = SearchForm()
    context = {
    }
  '''
  user = User.objects.get(username='14114031')
  context = {
    'user' : user,
    'is_logged_in' : True
  }'''
  return render(request,'connect/index.html',{'form':form})

def chat(request,receiver = None):
    if receiver == None:
        # user = request.user
        user = User.objects.get(username='14114031')
        latest = Chat.objects.filter(user = user).order_by('-datetime_created')[0]
        return HttpResponseRedirect('/chat/t/'+latest.other_user.username)
    else:
        user = User.objects.get(username='14114031')
        latest = Chat.objects.filter(user = user).order_by('-datetime_created')[:10]
        context = {
            'active' : user,
            'chat_users' : latest,
        }
        return render(request,'connect/chat.html',context)
        #One highlighted user
        #List of latest users on left
        #If highlighted matches any on left. cool =D

@login_required
def chat_request(request):
    try:
        student = Student.objects.get(user=request.user)
    except:
        return JsonResponse({"done":False, "message":"You're not a student"})
    try:
        alumni_id = request.POST.get("alumni_id")
        alumni = Alumni.objects.get(id=alumni_id)
    except:
        return JsonResponse({"done":False, "message":"Alumni with given id does not exist."})

    send_mail(alumni.email, "You're requested to chat with "+student+" go to url : "+"")
    return JsonResponse({"done":True, "message":"Email has been sent."})
