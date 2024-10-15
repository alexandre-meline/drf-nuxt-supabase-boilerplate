from django.db import models


class User(models.Model):
    """
    Représentation du modèle utilisateur alignée avec la table 'profiles' dans Supabase.
    
    Champs:
    - id: UUIDField primaire, non modifiable, utilisé pour identifier de manière unique chaque utilisateur.
    - first_name: CharField optionnel pour le prénom de l'utilisateur.
    - last_name: CharField optionnel pour le nom de famille de l'utilisateur.
    
    Meta:
    - db_table: Nom exact de la table dans Supabase.
    - managed: Défini à False pour ne pas inclure ce modèle dans les migrations gérées par Django.
    
    Propriétés:
    - is_authenticated: Toujours vrai, indiquant que l'utilisateur est authentifié dans le contexte des permissions Django.
    
    Usage typique:
    Utilisé pour identifier les utilisateurs, principalement dans des contextes d'authentification avec une intégration facile dans les systèmes externes comme Supabase Auth.
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
    Modèle que pour la lecture des abonnements utilisateurs, synchronisé avec 'UserSubscription' dans Supabase.
    Les champs sont mappés directement sur les colonnes de la table Supabase et la gestion des abonnement est géré sur le
    côté client.
    
    Champs:
    - id: Identifiant unique pour chaque abonnement, utilisé comme clé primaire.
    - user_id: Identifiant utilisateur unique associé, mappé à 'userId'.
    - stripe_customer_id: Identifiant optionnel du client dans Stripe.
    - stripe_subscription_id: Identifiant optionnel de l'abonnement dans Stripe.
    - stripe_price_id: Identifiant optionnel du prix d'abonnement dans Stripe.
    - stripe_current_period_end: DateTimeField qui dénote la fin de la période de renouvellement d'abonnement.
    
    Meta:
    - db_table: Correspond à la table 'UserSubscription' dans Supabase, sensibilité à la casse respectée.
    - managed: Défini à False car les ajustements structuraux sont gérés en dehors du cadre de Django.
    
    Usage typique:
    Ce modèle capture les informations des abonnements pour les interagir avec des systèmes de gestion de paiement comme Stripe, facilitant l'intégration et l'analyse métier.
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