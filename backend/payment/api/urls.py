from django.urls import path
from .views import (
    UserSubscriptionView,
    StripeWebhookView,
    UserSubscriptionStatusView
    )

urlpatterns = [
    path('subscription/', UserSubscriptionView.as_view(), name='subscription'),
    path('webhook/', StripeWebhookView.as_view(), name='webhook'),
    path('subscription/status/', UserSubscriptionStatusView.as_view(), name='subscription-status'),
]