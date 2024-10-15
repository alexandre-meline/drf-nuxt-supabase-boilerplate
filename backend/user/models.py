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
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = 'profiles'
        managed = False

    def __str__(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True
    