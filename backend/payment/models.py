from django.db import models
import uuid


class UserSubscription(models.Model):
    """
    Model for reading user subscriptions, synchronised with ‘UserSubscription’ in Supabase.
    Fields are mapped directly to columns in the Supabase table and subscription management is handled on the client side.
    client side.
    
    Fields:
    - id: Unique identifier for each subscription, used as primary key.
    - user_id: Associated unique user identifier, mapped to ‘userId’.
    - stripe_customer_id: Optional customer identifier in Stripe.
    - stripe_subscription_id: Optional subscription identifier in Stripe.
    - stripe_price_id: Optional identifier for the subscription price in Stripe.
    - stripe_current_period_end: DateTimeField denoting the end of the subscription renewal period.
    
    Meta:
    - db_table: Corresponds to the 'user_subscription' table in Supabase, case sensitive.
    
    Typical usage:
    This model captures subscription information to interact with payment management systems such as Stripe, facilitating integration and business analysis.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(unique=True)
    stripe_customer_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    stripe_subscription_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    stripe_price_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    stripe_current_period_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_subscription'  # Nom de la table doit refléter celui utilisé dans Supabase

    def __str__(self):
        return str(self.id)