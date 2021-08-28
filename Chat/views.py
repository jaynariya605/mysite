from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from Chat.models import PrivateChatRoom
from account.models import Account

# Create your views here.

def find_or_create_private_chat(request, session_ID):
	user1= None
	if request.user.is_authenticated:
		user1 = request.user
		try:
			chat = PrivateChatRoom.objects.get(user1=user1)
		except:
			chat = PrivateChatRoom(user1= user1,  session_ID= session_ID)
			chat.save()
	
	
		
	else:
	
		chat = PrivateChatRoom(user1= user1,  session_ID= session_ID)
		chat.save()
	

	return chat
def find_chat_roomlist(request):
	if request.user.is_admin:
		chat = PrivateChatRoom.objects.all()
	return chat


def Chat_home_view(request):


	if request.user.is_authenticated and request.user.is_admin:

		

		context={}
		rooms = find_chat_roomlist(request)
		m_and_f = []
		for room in rooms:
			friend = room.user1
			m_and_f.append({
				"message": "",
				"session_ID": room.session_ID,
				"friend": friend,
				})

		context['m_and_f'] = m_and_f
		context['debug_mode'] = settings.DEBUG

		return render(request, "Chat/chatadmin.html", context)




	else:


		context ={}
		context['debug_mode'] = settings.DEBUG
		s = SessionStore()
		s.create()
		session_ID = s.session_key
		

		if request.user.is_authenticated:
			if not request.user.is_admin:

				c =	find_or_create_private_chat(request,session_ID)
				context['session_ID'] = c.session_ID


		else:
			c =	find_or_create_private_chat(request,session_ID)
			context['session_ID'] = c.session_ID



		
		return render(request, "personal/home.html", context)