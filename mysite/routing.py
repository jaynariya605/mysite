from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from chatapp.consumer import PublicChatConsumer
from Chat.consumer import ChatConsumer


application =ProtocolTypeRouter({

	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(

			URLRouter([
				path("public_chat/<room_id>/", PublicChatConsumer.as_asgi()),
				path("private_chat/<session_ID>/", ChatConsumer.as_asgi()),

				])
			)
		)
	})