import jwt
from django.core.cache import cache
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User 

class JWTAuthentication(authentication.BaseAuthentication):
    """
    Authentication class for JWT management.
    This class is designed to extract and validate JWTs from authorisation headers
    from HTTP requests, decode these tokens to extract user information 
    and return an authenticated user if validations fail.
    
    Main methods:
    
    - authenticate(request): Extracts and checks the format of the JWT in the 
      HTTP HEADER. Calls _authenticate_credentials with the extracted token if present.
      
    - _authenticate_credentials(token): Decodes the JWT to verify the user.
      Uses cache to optimise repeated searches. Throws exceptions 
      if verification fails.
    Details of Errors:
    
    - AuthenticationFailed: Raised if the token is incorrectly formed, expired, or 
      invalid, or if the corresponding user is not found in the database. 
      database.

    Typical use:
    Implement this middleware in your REST framework authentication pipeline 
    to manage endpoint security using JWT provided by 
    the Supabase authentication system.
    - Using: ‘DEFAULT_AUTHENTICATION_CLASSES’: (
                        user.authentication.JWTAuthentication',
                    ),
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

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

           user = cache.get(user_id)
           if not user:
               user = User.objects.get(id=user_id)
               cache.set(user_id, user, timeout=300)

       except jwt.ExpiredSignatureError:
           raise exceptions.AuthenticationFailed('Token expired.')
       except jwt.InvalidTokenError:
           raise exceptions.AuthenticationFailed('Invalid token.')
       except User.DoesNotExist:
           raise exceptions.AuthenticationFailed('User not found.')

       return (user, token)