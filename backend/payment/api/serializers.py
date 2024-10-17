# Serializers.py
from rest_framework import serializers
from payment.models import UserSubscription


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = '__all__'