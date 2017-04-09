from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from connect.models import *
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import SearchForm

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/done')

@login_required
def index(request):
  if request.method == 'POST':
    form = SearchForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      branch = form.cleaned_data['branch']
      batch = form.cleaned_data['batch']
      tags = form.cleaned_data['tags']
      alumni = Alumni.objects.filter(user__name__icontains = name, branch = branch, passout_year = batch, tags__name__in = tags)
      context = {
        'form': form,
        'alumni': alumni,
      }
    else:
      form = SearchForm()
      context = {
        'form': form
      }
    return render(request, 'connect/index.html', context)
  else:
    form = SearchForm()
    context = {
    }
  return render(request,'connect/index.html',{'form':form})

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
@login_required
def chat_alumni(request, chat_ekey):
    print chat_ekey
    try:
        chat_request = ChatRequest.objects.get_by_ekey(chat_ekey)
    except Exception as e:
      print e
      return HttpResponse('Not a valid link')
    else:
        return redirect("/chat/" + chat_request.sender.username) 


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


def chat(request,rcvr):
  receiver = User.objects.get(username = rcvr)
  user = request.user
  messages= Chat.objects.filter(Q(sender = user, receiver = receiver) | Q(sender = receiver, receiver = user)).order_by('-datetime_created')[:30]
  return render(request, 'connect/chat.html',{'messages':messages,'user':user,'receiver':receiver})
