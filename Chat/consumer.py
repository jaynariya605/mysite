from django.core.serializers.python import Serializer
from django.core.paginator import Paginator
from django.core.serializers import serialize
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils import timezone
from datetime import datetime
from Chat.utils import LazyAccountEncoder, calculate_timestamp, LazyRoomChatMessageEncoder, ClientError
from Chat.models import PrivateChatRoom, RoomChatMessage



MSG_TYPE_MESSAGE = 0
DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE = 10
MSG_TYPE_ENTER =1
MSG_TYPE_LEAVE= 2




class ChatConsumer(AsyncJsonWebsocketConsumer):


	async def connect(self):
		
		print("ChatConsumer: connect: " + str(self.scope["user"]))

		await self.accept()
		
		self.session_ID = None


		

	async def receive_json(self, content):
		
		print("ChatConsumer: receive_json")
		command = content.get("command", None)

		try:
			if command == "join":
				await self.join_room(content['session_ID'])
				print("ChatConsumer: receive_join")
			elif command == "leave":
				await self.leave_room(content['session_ID'])
				
			elif command == "send":
				print("ChatConsumer: receive_send")
				if len(content['message'].lstrip())==0:
					raise Exception("Empty message")
				await self.send_room(content['session_ID'], content['message'])
				
			elif command == "get_room_chat_messages":
				print("ChatConsumer: receive_get_room_chat_messages")
				room = await get_room_or_eroor(content['session_ID'])
				
				print("ChatConsumer: got room")
				
				payload = await get_room_chat_messages(room, content['page_number'])
				print("got payload")
				
				if payload != None:
					
					payload = json.loads(payload)
					await self.send_messages_payload(payload['messages'], payload['new_page_number'])
					

				else:
					raise ClientError(204, "something wrong")


			elif command == "get_user_info":
				session_ID = content['session_ID']
				payload = await get_user_info(session_ID)
				if payload != None:
					payload = json.loads(payload)
					await self.send_user_info_payload(payload['user_info'])
				else:
					raise Exception("askdgfusgdfcskjdhg")


			elif command == "close":
				print("Hey I got what you wanted")
		except Exception as e:
			pass



	async def disconnect(self, code):
		
		print("ChatConsumer: disconnect")

		

		try:
			if self.session_ID != None:
				await self.leave_room(self.session_ID)
		except Exception as e:
			pass








	async def join_room(self, session_ID):
	
		print("ChatConsumer: join_room: " + str(session_ID))
		try:
			room = await get_room_or_eroor(session_ID)
		except Exception as e:
			return

		room = await get_room_or_eroor(session_ID)



		await self.channel_layer.group_add(
			room.group_name,
			self.channel_name
			)

		await self.send_json({
			"join": str(session_ID)
			})

		await self.channel_layer.group_send(
			room.group_name,
			{
			"type": "chat.join",
			"session_ID":session_ID,
			"username": self.scope['user'].username,

			}
			)



	async def leave_room(self, session_ID):
		
		

		room = await get_room_or_eroor(session_ID)

		await self.channel_layer.group_send(
			room.group_name,
			{
			"type": "chat.leave",
			"session_ID": session_ID,
			"username" : self.scope['user'].username,
			}
			)

		self.session_ID = None
		await self.channel_layer.group_discard(
			room.group_name,
			self.channel_name
			)

		await self.send_json({
			"leave": str(session_ID)
			})



	async def send_room(self, session_ID, message):
		
		print("ChatConsumer: send_room")

		
	
		room = await get_room_or_eroor(session_ID)
		
		print(room.group_name)
		
			
		

		await create_room_chat_message(room, self.scope['user'],message)
		print("created chat room")
		

		await self.channel_layer.group_send(
			room.group_name,
			{
			"type": "chat.message",
			"username": self.scope['user'].username,
			"message": message,
			"session_ID": session_ID
			}
			)

		print("sent successful")

	# These helper methods are named by the types we send - so chat.join becomes chat_join
	async def chat_join(self, event):
		
		print("ChatConsumer: chat_join: " + str(self.scope["user"].id))
		if event['username']:
			await self.send_json({
				"msg_type": MSG_TYPE_ENTER,
				"session_ID": event['session_ID'],
				"username": event['username'],
				"message": event['username'] + "" + " connected",
				
				})


	async def chat_leave(self, event):

		print("ChatConsumer: chat_leave")

		if event['username']:
			await self.send_json({
				"msg_type": MSG_TYPE_LEAVE,
				"session_ID": event['session_ID'],
				"username": event['username'],
				"message": event['username'] +""+ " disconnected",
				
				})



	async def chat_message(self, event):
		
		print("ChatConsumer: chat_message")

		timestamp = calculate_timestamp(timezone.now())
		if(event['username'] != ""):
			

			await self.send_json({
				"msg_type": MSG_TYPE_MESSAGE,
				"username": event['username'],
				"message": event['message'],
				"natural_timestamp": timestamp,
				"session_ID": event['session_ID']


				})
		else:
			await self.send_json({
				"msg_type": MSG_TYPE_MESSAGE,
				"username": "Anonymous",
				"message": event['message'],
				"natural_timestamp": timestamp,
				"session_ID": event['session_ID']


				})



	async def send_messages_payload(self, messages, new_page_number):
		
		print("ChatConsumer: send_messages_payload. ")

		await self.send_json({
			"messages_payload": "messages_payload",
			"messages": messages,
			"new_page_number": new_page_number
			})


	async def send_user_info_payload(self, user_info):
		
		
		await self.send_json({
			'user_info' : user_info
			})





@database_sync_to_async
def get_room_or_eroor(session_ID):


	try:
		room = PrivateChatRoom.objects.get(session_ID=session_ID)
		
	except:
		raise Exception("INvalid room.")



	return room



@database_sync_to_async

def get_user_info(session_ID):
	

	room = PrivateChatRoom.objects.get(session_ID=session_ID)
	user1 = room.user1
	payload={}
	s = LazyAccountEncoder()

	if (user1 != None):

		
		payload['user_info'] = s.serialize([user1])[0]
	else:
		payload['user_info'] = {
		'email': "Anonymous",
		'username':"Anonymous" 

		}

	return json.dumps(payload)




@database_sync_to_async

def create_room_chat_message(room ,user, message):
	if not user.is_anonymous:
		
		return RoomChatMessage.objects.create( user = user,room=room, content =message)
	else:
		

		return RoomChatMessage.objects.create(room=room, content =message)



@database_sync_to_async
def get_room_chat_messages(room, page_number):

	try:
		qs = RoomChatMessage.objects.by_room(room)

		p = Paginator(qs, DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE)
		
		

		payload ={}

		

		new_page_number = int(page_number)
		if new_page_number <= p.num_pages:
			new_page_number = new_page_number + 1
			s = LazyRoomChatMessageEncoder()
			payload['messages'] = s.serialize(p.page(page_number).object_list)
			

		else:
			payload['messages'] = "None"
		payload['new_page_number'] =  new_page_number
		return json.dumps(payload)

	except Exception as e:
		print("Exception" +str(e))
		return None

