"""
The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from connect import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^$', views.index),
  url(r'^advanced/$', views.advanced),
  url(r'^login/$', auth_views.login,{'template_name':'connect/login.html'}),
  url(r'^logout/$', views.logout_view, name='logout'),
  url(r'^chat_request/$', views.chat_request_view),
  url(r'^chat_alumni/(?P<chat_ekey>[0-9a-zA-Z-_]+.{0,2})/$', views.chat_alumni),
  url(r'^messages/(?P<rcvr>[0-9]{8})/$',views.messages),
  url(r'^student_chat/$',views.student_chat),
  url(r'^student_chat/(?P<target>[0-9]+)/$',views.student_chat),
  url(r'^chat_list/$',views.chat_list),
  url(r'^chat_user_list/$', views.chat_user_list),
  url(r'^message/$',views.add_message)
]
