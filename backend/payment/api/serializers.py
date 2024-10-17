# Serializers.py
from rest_framework import serializers
from payment.models import UserSubscription


class UserSubscriptionSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=200)

class UserSubscriptionStatusSerializer(serializers.Serializer):
    subscribed = serializers.BooleanField()