""" User urls """
from django.urls import path

from user import views

app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('messages/', views.ManageUserMessageView.as_view(), name='message'),
    path('linkedin/', views.LinkedinAPIView.as_view(), name='linkedin'),
    path('me1/', views.UserRetrieveView.as_view(), name='me1'),
    path('me2/', views.UserRetrieveView2.as_view(), name='me2'),
]
