from django.shortcuts import render
from django.conf import settings
# Create your views here.

DEBUG = False
def Chat_home_view(request):

	context ={}
	context['debug_mode'] = settings.DEBUG
	context['room_id'] = 1 
	context['debug'] = DEBUG

	return render(request, "chatapp/chathome.html", context)