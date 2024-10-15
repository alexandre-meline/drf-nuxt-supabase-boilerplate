import jwt
from django.core.cache import cache
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User 

class JWTAuthentication(authentication.BaseAuthentication):
    """
    Classe d'authentification pour la gestion des JWT.

    Cette classe est conçue pour extraire et valider les JWT des en-têtes d'autorisation
    des requêtes HTTP, décoder ces tokens pour extraire les informations utilisateur, 
    et retourner un utilisateur authentifié si les validations échouent.
    
    Méthodes principales:
    
    - authenticate(request): Extrait et vérifie le format du JWT dans l'en-tête 
      HTTP. Appelle _authenticate_credentials avec le token extrait s'il est présent.
      
    - _authenticate_credentials(token): Décodage du JWT pour vérifier l'utilisateur.
      Utilise le cache pour optimiser les recherches répétées. Lève des exceptions 
      en cas d'échec de la vérification.

    Détails des Erreurs:
    
    - AuthenticationFailed: Est levée si le token est mal formé, expiré, ou 
      invalide, ou si l'utilisateur correspondant n'est pas trouvé dans la base 
      de données.

    Utilisation typique:
    Implémenter ce middleware dans votre pipeline d'authentification REST framework 
    pour gérer la sécurisation des endpoints à l'aide de JWT fournis par 
    le système d'authentification de Supabase.
    - En utilisant: 'DEFAULT_AUTHENTICATION_CLASSES': (
                        'user.authentication.JWTAuthentication',
                    ),
    """
    def authenticate(self, request):
        # Obtient le header d'authentification
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        # Valide le format du header
        try:
            # Expected Header: "Bearer <token>"
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Bearer token malformed.')
                
        except ValueError:
            raise exceptions.AuthenticationFailed('Authorization header must contain two space-separated values')

        return self._authenticate_credentials(token)

    def _authenticate_credentials(self, token):
       try:
           payload = jwt.decode(
               jwt=token, 
               key=settings.SUPABASE_JWT_SECRET, 
               algorithms=["HS256"], 
               audience="authenticated"
               )
           
           user_id = payload.get('sub')

           # Vérifier si l'utilisateur est déjà dans le cache
           user = cache.get(user_id)
           if not user:
               # Si non dans le cache, récupérer depuis la base de données
               user = User.objects.get(id=user_id)
               # Mettre l'utilisateur en cache pour un certain temps (ex : 300 secondes)
               cache.set(user_id, user, timeout=300)

       except jwt.ExpiredSignatureError:
           raise exceptions.AuthenticationFailed('Token expired.')
       except jwt.InvalidTokenError:
           raise exceptions.AuthenticationFailed('Invalid token.')
       except User.DoesNotExist:
           raise exceptions.AuthenticationFailed('User not found.')

       return (user, token)