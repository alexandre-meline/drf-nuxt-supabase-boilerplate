# Urls
from django.urls import path
from .views import UserProfileAPIView, UserWebhookView

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('webhook/', UserWebhookView.as_view(), name='webhook'),

]