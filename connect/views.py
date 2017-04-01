from django.shortcuts import render,HttpResponse
from connect.models import *
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

def index(request):
	user = User.objects.get(username='14114031')

	context = {
		'user' : user,
		'is_logged_in' : True
	}
	return render(request,'connect/index.html',context)

@csrf_exempt
def node_api(request):
    try:
        #Get User from sessionid
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(id=user_id)
        #Create comment
        Comments.objects.create(user=user, text=request.POST.get('comment'))
        #Once comment has been created post it to the chat channel
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('chat', user.username + ': ' + request.POST.get('comment'))
        return HttpResponse("Everything worked :)")
    except Exception, e:
        return HttpResponse(str(e))
