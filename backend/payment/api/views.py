import pytz
import stripe
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from payment.models import UserSubscription
from .serializers import (
    UserSubscriptionSerializer, 
    UserSubscriptionStatusSerializer
    )
from core.utils import splitting_var_env
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
    )

stripe.api_key = settings.STRIPE_SECRET_KEY


class UserSubscriptionView(APIView):
    serializer = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        price_id = request.data.get('price_id')

        if not price_id:
            raise APIException("price_id is required", code=400)

        try:
            user_subscription = UserSubscription.objects.get(user_id=user.id)
        except UserSubscription.DoesNotExist:
            user_subscription = None

        returnUrl = settings.FRONTEND_URL
        successUrl = settings.STRIPE_SUCCESS_URL
        cancelUrl = settings.STRIPE_CANCEL_URL
        payment_methods = splitting_var_env(var_env=settings.STRIPE_PAYMENT_METHODS)

        # If the user has a subscription, redirect them to the billing portal
        if user_subscription and user_subscription.stripe_customer_id:
            stripe_session = stripe.billing_portal.Session.create(
                customer=user_subscription.stripe_customer_id,
                return_url=returnUrl
            )
            serializer = self.serializer({'url': stripe_session.url})
            return Response(serializer.data, status=200)

        stripe_session = stripe.checkout.Session.create(
            success_url=successUrl,
            cancel_url=cancelUrl,
            payment_method_types=payment_methods,
            mode='subscription',
            billing_address_collection='auto',
            customer_email=user.email,
            automatic_tax={'enabled': True},
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1
                }
            ],
            metadata={
                'user_id': str(user.id),
            }
        )
        serializer = self.serializer({'url': stripe_session.url})

        return Response(serializer.data, status=200)
    

class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None

        # Verify webhook signature
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_KEY
            )
        except ValueError as e:
            # Invalid payload
            return Response({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response({'error': 'Invalid signature'}, status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            self.handle_checkout_session(session)

        elif event['type'] == 'customer.subscription.updated':
            subscription = event['data']['object']
            self.handle_subscription_update(subscription)

        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            self.handle_subscription_deletion(subscription)

        # Add more event types if needed

        return Response({'status': 'success'}, status=200)

    def handle_checkout_session(self, session):
        """Handle checkout session completion event."""
        try:
            subscription = stripe.Subscription.retrieve(session['subscription'])
        
            naive_datetime = datetime.fromtimestamp(subscription['current_period_end'])
            aware_datetime = timezone.make_aware(naive_datetime, timezone=pytz.timezone(settings.TIME_ZONE))

            UserSubscription.objects.create(
                user_id=session['metadata']['user_id'],
                stripe_subscription_id=subscription['id'],
                stripe_customer_id=subscription['customer'],
                stripe_price_id=subscription['items']['data'][0]['price']['id'],
                stripe_current_period_end=aware_datetime)
            return Response({'status': 'success'}, status=200)
        except Exception as e:
            print(f"Error processing checkout session: {e}")
            return Response({'error': 'Error processing checkout session'}, status=400)
    
    def handle_subscription_update(self, subscription):
        """Handle subscription update event."""
        try:
            naive_datetime = datetime.fromtimestamp(subscription['current_period_end'])
            aware_datetime = timezone.make_aware(naive_datetime, timezone=pytz.timezone(settings.TIME_ZONE))

            user_subscription = UserSubscription.objects.get(
                stripe_subscription_id=subscription['id']
                )
            user_subscription.stripe_price_id = subscription['items']['data'][0]['price']['id']
            user_subscription.stripe_current_period_end = aware_datetime
            user_subscription.save()
            return Response({'status': 'success'}, status=200)
        except ObjectDoesNotExist:
            print("Subscription does not exist.")
            return Response({'error': 'Subscription does not exist'}, status=400)
        except Exception as e:
            print(f"Error updating subscription: {e}")
            return Response({'error': 'Error updating subscription'}, status=400)

    def handle_subscription_deletion(self, subscription):
        """Handle subscription deletion event."""
        try:
            UserSubscription.objects.filter(
                stripe_subscription_id=subscription['id']
            ).delete()
            return Response({'status': 'success'}, status=200)
        except Exception as e:
            print(f"Error deleting subscription: {e}")
            return Response({'error': 'Error deleting subscription'}, status=400)


DAY_IN_MS = 86400000  # Miliseconds in a day

class UserSubscriptionStatusView(APIView):
    serializer = UserSubscriptionStatusSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"user_subscription_status_{user.id}"

        # Vérifier si résult est en cache
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            serializer = UserSubscriptionStatusSerializer(data={'subscribed': cached_result})
            if serializer.is_valid():
                return Response(serializer.data, status=200)

        try:
            user_subscription = UserSubscription.objects.only(
                'stripe_subscription_id', 'stripe_current_period_end',
                'stripe_customer_id', 'stripe_price_id'
            ).get(user_id=user.id)
        except ObjectDoesNotExist:
            cache.set(cache_key, False, timeout=60*2)
            return Response({'subscribed': False})
        except Exception as e:
            print('Error fetching user subscription:', e)
            raise APIException('Internal Server Error')

        is_valid = self.is_valid_subscription(
            user_subscription.stripe_price_id,
            user_subscription.stripe_current_period_end
        )

        cache.set(cache_key, is_valid, timeout=60*2)

        serializer = UserSubscriptionStatusSerializer(data={'subscribed': is_valid})
        if serializer.is_valid():
            return Response(serializer.data, status=200)

    def is_valid_subscription(self, stripe_price_id, stripe_current_period_end):
        if not stripe_price_id or not stripe_current_period_end:
            return False
        expiry_time = stripe_current_period_end.timestamp() + (DAY_IN_MS / 1000)  # Convert milliseconds to seconds
        return expiry_time > datetime.now().timestamp()