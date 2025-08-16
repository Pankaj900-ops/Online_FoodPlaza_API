
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        # Minimal registration: create user + customer
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        mobile = request.data.get('mobile')
        if not username or not password:
            return Response({'code':'missing_fields','message':'username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        customer = self.get_serializer().Meta.model.objects.create(user=user, name=name or username, mobile=mobile or '')
        return Response({'id': customer.id, 'username': user.username})
