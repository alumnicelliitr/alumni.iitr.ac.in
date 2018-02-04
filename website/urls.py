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
from website import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^samp$', views.samp_index),
	url(r'^samp/$', views.samp_index),
	url(r'^card$',views.alumnicard),
	url(r'^card/$',views.alumnicard),
	url(r'^distinguished$', views.distinguishedformnew),
	url(r'^distinguished/$', views.distinguishedformnew),
	url(r'^unsubscribe/(?P<key>(.*))/$',views.unsubscribe, name='unsubscribe'),
	url(r'^resubscribe/(?P<key>(.*))/$',views.resubscribe, name='resubscribe'),
	url(r'^updatesubscriberprofile/(?P<key>(.*))/$', views.update_profile, name='update'),
	url(r'^send/(?P<id>[0-9]+)/$', views.send_mail, name='sendmsg'),
	url(r'^(?P<level0>[a-z]+)$',views.level),
	url(r'^(?P<level0>[a-z]+)/(?P<level1>[a-z]+)$',views.level),
	url(r'^(?P<level0>[a-z]+)/(?P<level1>[a-z]+)/(?P<level2>[a-z]+)$',views.level)
]
