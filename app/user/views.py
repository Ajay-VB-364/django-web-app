"""
Views for User API
"""
import json
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    MessageSerializer,
    LinkedinSerializer,
)
from rest_framework.response import Response
from constants.whatsapp import TEMPLATES
from utils.whatsapp import WhatsAppIntegration
from utils.linkedin import LinkedInService


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


class LinkedinAPIView(generics.CreateAPIView):
    """ Send Whats App message """
    serializer_class = LinkedinSerializer

    def create(self, request):
        req = json.loads(request.body)
        username = req['username'] or None
        password = req['password'] or None
        company = req['company'] or None

        data = {}

        if username and password:
            try:
                linkedin = LinkedInService(username=username, password=password)
                api = linkedin.get_linkedin_api()
                comp_data = linkedin.get_linkedin_company_details(api=api, company=company)
                data['linkedin_company_details'] = comp_data
                data['success'] = True
                data['message'] = 'Linkedin company details fetched successfully'
            except Exception as e:
                data['success'] = False
                data['message'] = str(e)
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data=data, status=status.HTTP_200_OK)


from utils.decorators import user_role_check
from rest_framework.views import APIView


class UserRetrieveView(APIView):
    """ Get user data from system """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @user_role_check(['is_support', 'is_staff'])
    def get(self, request):
        """ retrieve and return authenticated user """
        data = {}
        data['name'] = request.user.name
        return Response(data=data, status=status.HTTP_200_OK)



from rest_framework import generics, authentication, permissions, status
from user.serializers import UserSerializer
from utils.decorators import user_role_check


class UserRetrieveView2(generics.RetrieveAPIView):
    """ Get user data from system """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @user_role_check(['is_support', 'is_staff'])
    def get(self, request):
        """ retrieve and return authenticated user """
        data = {}
        data['user'] = request.user.name
        return Response(data=data, status=status.HTTP_200_OK)
