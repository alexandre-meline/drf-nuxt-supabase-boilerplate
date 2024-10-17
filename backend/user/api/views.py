# Create vue for user profile APIview get
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from user.models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny


class UserProfileAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        secret = request.headers.get('X-Supabase-Secret')
        if secret != settings.SUPABASE_WEBHOOK_SECRET:
            return Response(status=status.HTTP_403_FORBIDDEN)

        event_type = request.data.get('type')
        table = request.data.get('table')
        schema = request.data.get('schema')
        user_id = request.data.get('old_record').get('id')
        
        if not user_id:
            return Response({"detail": "User ID is missing."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle user deletion
        if event_type == 'DELETE' and table == 'users' and schema == 'auth':
            return self.handle_user_deletion(user_id)

        # Add more event handling (like updates) as necessary
        
        return Response(status=status.HTTP_200_OK)
    
    def handle_user_deletion(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
