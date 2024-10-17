import jwt
from django.core.cache import cache
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import CustomUser 

class JWTAuthentication(authentication.BaseAuthentication):
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
                try:
                    # Try to get the user from the database
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    # If the user does not exist, create a new one
                    user_email = payload.get('email', '')
                    user = CustomUser.objects.create(
                        id=user_id,
                        email=user_email,
                        is_active=True
                    )
                # Cache the user to avoid repeat database queries
                cache.set(user_id, user, timeout=300)
                
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return (user, token)