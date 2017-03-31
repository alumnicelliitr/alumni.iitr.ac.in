from django.shortcuts import render,HttpResponse
from connect.models import *
# Create your views here.

def index(request):
	user = User.objects.get(username='14114031')

	context = {
		'user' : user,
		'is_logged_in' : True
	}
	return render(request,'connect/index.html',context)