from django.urls import path
from .views import createUserAPIView, AuthenticateUserAPIView, sportsItemsAPIView, favSportsAPIView, getUserList, brodcastMessagesAPIView

urlpatterns = [
    path('register',createUserAPIView.as_view(),name="register"),
    path('login', AuthenticateUserAPIView.as_view(),name="login"),
    path('sportsList', sportsItemsAPIView.as_view(),name="sportsList"),
    path('sports', favSportsAPIView.as_view(),name="sports"),
    path('users', getUserList.as_view(),name="users"),
    path('brodcast', brodcastMessagesAPIView.as_view(),name="brodcast"),
]