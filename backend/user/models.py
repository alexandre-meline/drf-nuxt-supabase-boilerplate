from django.db import models


class User(models.Model):
    """
    Representation of the user model aligned with the ‘profiles’ table in Supabase.
    
    Fields:
    - id: Primary, unmodifiable UUIDField used to uniquely identify each user.
    - first_name: Optional CharField for the user's first name.
    - last_name: Optional charField for the user's surname.
    
    Meta:
    - db_table: Exact name of the table in Supabase.
    - managed: Set to False to not include this model in Django managed migrations.
    
    Properties:
    - is_authenticated: Always true, indicating that the user is authenticated in the context of Django permissions.
    
    Typical usage:
    Used to identify users, primarily in authentication contexts with easy integration into external systems such as Supabase Auth.

    """
    id = models.UUIDField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'profiles'
        managed = False

    def __str__(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True
    
    
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
    - db_table: Corresponds to the ‘UserSubscription’ table in Supabase, case sensitive.
    - managed: Set to False because structural adjustments are handled outside the Django framework.
    
    Typical usage:
    This model captures subscription information to interact with payment management systems such as Stripe, facilitating integration and business analysis.
    """
    id = models.CharField(primary_key=True, max_length=200)
    user_id = models.CharField(unique=True, max_length=200, db_column='userId')
    stripe_customer_id = models.CharField(unique=True, max_length=200, null=True, blank=True, db_column='stripe_customer_id')
    stripe_subscription_id = models.CharField(unique=True, max_length=200, null=True, blank=True, db_column='stripe_subscription_id')
    stripe_price_id = models.CharField(unique=True, max_length=200, null=True, blank=True, db_column='stripe_price_id')
    stripe_current_period_end = models.DateTimeField(null=True, blank=True, db_column='stripe_current_period_end')

    class Meta:
        db_table = 'UserSubscription'  # Nom de la table doit refléter celui utilisé dans Supabase
        managed = False

    def __str__(self):
        return self.id