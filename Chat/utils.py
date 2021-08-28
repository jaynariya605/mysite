from django.core.serializers.python import Serializer
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils import timezone
from datetime import datetime


MSG_TYPE_MESSAGE = 0
class LazyAccountEncoder(Serializer):
	def get_dump_object(self,obj):
		dump_object = {}
		dump_object.update({'email': str(obj.email)})
		dump_object.update({'username': str(obj.username)})

		return dump_object


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


		

class LazyRoomChatMessageEncoder(Serializer):
	def get_dump_object(self, obj):
		dump_object = {}
		dump_object.update({'msg_type': MSG_TYPE_MESSAGE})
		dump_object.update({'username': str(obj.user.username)})
		dump_object.update({'message': str(obj.content)})
		dump_object.update({'natural_timestamp': calculate_timestamp(obj.timestamp)})
		return dump_object