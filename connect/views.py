from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from connect.models import *
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

def index(request):
	user = User.objects.get(username='14114031')
	context = {
		'user' : user,
		'is_logged_in' : True
	}
	return render(request,'connect/index.html',context)

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
