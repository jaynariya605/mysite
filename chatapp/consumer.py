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

from chatapp.models import PublicChatRoom, PublicRoomChatMessage


MSG_TYPE_MESSAGE = 0
DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE = 10


User = get_user_model()


class PublicChatConsumer(AsyncJsonWebsocketConsumer):

	async def connect(self):

		print("PublicChatConsumer: connct:" + str(self.scope['user']))

		await self.accept()
		self.room_id = None

		






	async def disconnect(self,code):

		print("PublicChatConsumer: disconnect")
		try:
			if self.room_id != None:
				await self.leave_room(self.room_id)

		except Exception:
			pass





	async def receive_json(self, content):



		command = content.get("command", None)
		
		print("PublicChatConsumer: receive_json:" +str(command))
		try:
			if command =="send":
				if len(content['message'].lstrip()) != 0:
					#raise ClientError(422, "You cant send an empty message")
					await self.send_room(content['room_id'],content['message'])


			elif command =="join":
				await self.join_room(content['room'])

			elif command =="leave":
				await self.leave_room(content['room'])
			elif command =="get_room_chat_messages":
				room = await get_room_or_eroor(content['room_id'])
				payload = await get_room_chat_messages(room, content['page_number'])
				if payload != None:
					payload = json.loads(payload)
					await self.send_messages_payload(payload['messages'], payload['new_page_number'])

				else:
					raise ClientError(204, " somthing went wrong retriving chatrooms")
		except ClientError as e:
			await self.handle_client_eroor(e)

	


	async def send_room(self, room_id, message):


		print("PublicChatConsumer: send_room")


		if self.room_id != None:
			if str(room_id) != str(self.room_id):
				raise ClientError("Room_Acc_Denied", "Rooom acce denied")

			if not is_authenticated(self.scope['user']):
				raise ClientError("AUTH_ERROR", "Youy  are not authenticated")

		else:
			raise ClientError("Room_Acc_Denied", "Rooom acce denied")


		room = await get_room_or_eroor(room_id)
		await create_public_room_chat_message(room, self.scope['user'], message)

		await self.channel_layer.group_send(
			room.group_name,
			{
			"type" : "chat.message", #chat_message
			#'profile_image': self.scope['user'].profile_image.url,
			'username': self.scope['user'].username,
			'user_id': self.scope['user'].id,
			'message': message,
			}
		)



	async def chat_message(self, event):


		print("PublicChatConsumer: chat_message from user #:" + str(event['user_id']))
		timestamp = calculate_timestamp(timezone.now())
		await self.send_json({
			#"profile_image": event['profile_image'],
			"msg_type" : MSG_TYPE_MESSAGE,
			"username": event['username'],
			"user_id": event['user_id'],
			"message": event['message'],
			"natural_timestamp": timestamp,
			})



	async def join_room(self, room_id):

		print("Public Chat consumer: Join_jason")
		is_auth = is_authenticated(self.scope['user'])
		try: 
			room = await get_room_or_eroor(room_id)
		except ClientError as e:
			await self.handle_client_eroor(e)


		if is_auth:
			await connect_user(room, self.scope['user'])

		self.room_id = room.id


		await self.channel_layer.group_add(
			room.group_name,
			self.channel_name,
			)



		await self.send_json({
			"join": str(room.id)
			
			})



	async def leave_room(self, room_id):


		print("PublicChatConsumer: leave_room")


		is_auth = is_authenticated(self.scope['user'])

		
		room = await get_room_or_eroor(room_id)
		

		if is_auth:
			await disconnect_user(room, self.scope['user'])


		self.room_id = None



		await self.channel_layer.group_discard(
			room.group_name,
			self.channel_name
			)


	async def send_messages_payload(self,messages, new_page_number):


		print("PublicChatConsumer: send_messages_payload")
		await self.send_json({
			"messages_payload": "messages_payload",
			"messages" : messages,
			"new_page_number": new_page_number,
			})



	async def handle_client_eroor(self, e):

		errorData = {}
			
		errorData['error']= e.code
		if e.message:
			errorData['message']= e.message

			await self.send_json(errorData)
		return


@database_sync_to_async
def create_public_room_chat_message( room, user, message):
	return PublicRoomChatMessage.objects.create(user =user, room = room, content = message)




@database_sync_to_async
def connect_user(room, user):
	return room.connect_user(user)

@database_sync_to_async
def disconnect_user(room, user):
	return room.disconnect_user(user)


@database_sync_to_async
def get_room_or_eroor(room_id):

	try:
		room = PublicChatRoom.objects.get(pk=room_id)

	except PublicChatRoom.DoesNotExist:
		raise ClientError("ROOM_INVALID", "INvalid Room")
	return room


def is_authenticated(user):     
	if user.is_authenticated:
		return True
	return False


def calculate_timestamp(timestamp):

	ts=""

	if ((naturalday(timestamp) == "today") or (naturalday(timestamp) == "yesterday")):
		str_time = datetime.strftime(timestamp, "%I:%M %p")
		str_time =str_time.strip("0") #remove zero from time
		ts = f"{naturalday(timestamp)} at {str_time}"

	else:
		str_time = datetime.strftime(timestamp, "%m/%d/%Y")
		ts = f"{str_time}"

	return ts

class ClientError(Exception):



	def  __init__(self, code, message):
		super().__init__(code)
		self.code = code
		if message:
			self.message = message



@database_sync_to_async
def get_room_chat_messages(room, page_number):

	try:
		qs = PublicRoomChatMessage.objects.by_room(room)
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




class LazyRoomChatMessageEncoder(Serializer):
	def get_dump_object(self, obj):
		dump_object = {}
		dump_object.update({'msg_type': MSG_TYPE_MESSAGE})
		dump_object.update({'user_id': str(obj.user_id)})
		dump_object.update({'username': str(obj.user.username)})
		dump_object.update({'message': str(obj.content)})
		dump_object.update({'natural_timestamp': calculate_timestamp(obj.timestamp)})
		return dump_object