"""
Views for User API
"""
import json
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    MessageSerializer,
)
from rest_framework.response import Response
from constants.whatsapp import TEMPLATES
from utils.whatsapp import WhatsAppIntegration

class CreateUserView(generics.CreateAPIView):
    """ Create a new user in system """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new user in system """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Get and Update a new user in system """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ retrieve and return authenticated user """
        return self.request.user

from rest_framework import status

class ManageUserMessageView(generics.CreateAPIView):
    """ Send Whats App message """
    serializer_class = MessageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        req = json.loads(request.body)
        country = req['country_code'] or None
        whatsapp = req['whatsapp'] or None
        content = req['content'] or None
        template = TEMPLATES['CONTENT']

        whatsapp = WhatsAppIntegration()
        flag, message = whatsapp.send_whatsapp_message(
            country_code=country, 
            buyer_number=whatsapp, 
            template_name=template,
            content=content
            )
        
        data = {}
        data['success'] = False
        data['message'] = message
        if flag:
            data['success'] = True
        
        return Response(data=data, status=status.HTTP_200_OK)

